"""
Web scraping utilities for extracting job ads from URLs.
"""

from typing import Optional, Dict, Any
from urllib.parse import urlparse
import re

try:
    import requests
    from bs4 import BeautifulSoup
    _HAS_SCRAPING = True
except ImportError:
    _HAS_SCRAPING = False


class JobAdScraper:
    """
    Extract job descriptions from various job board URLs.
    
    Supports:
    - LinkedIn
    - Indeed
    - Glassdoor
    - Generic websites
    """
    
    def __init__(self, timeout: int = 10):
        """
        Initialize scraper.
        
        Args:
            timeout: Request timeout in seconds.
        """
        if not _HAS_SCRAPING:
            raise ImportError(
                "Web scraping requires additional dependencies. "
                "Install with: pip install requests beautifulsoup4"
            )
        
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        Scrape job ad from URL.
        
        Args:
            url: URL of the job posting.
            
        Returns:
            Dictionary with 'text', 'title', 'company', 'url', 'source'.
        """
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Determine source and use appropriate extractor
        if 'linkedin.com' in domain:
            return self._scrape_linkedin(url)
        elif 'indeed.com' in domain:
            return self._scrape_indeed(url)
        elif 'glassdoor.com' in domain:
            return self._scrape_glassdoor(url)
        else:
            return self._scrape_generic(url)
    
    def _fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse HTML page."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch URL: {e}")
    
    def _scrape_linkedin(self, url: str) -> Dict[str, Any]:
        """Extract job ad from LinkedIn."""
        soup = self._fetch_page(url)
        
        # Extract title
        title_elem = soup.find('h1', class_='top-card-layout__title')
        title = title_elem.get_text(strip=True) if title_elem else "Unknown Position"
        
        # Extract company
        company_elem = soup.find('a', class_='topcard__org-name-link')
        if not company_elem:
            company_elem = soup.find('span', class_='topcard__flavor')
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        
        # Extract description
        desc_elem = soup.find('div', class_='show-more-less-html__markup')
        if not desc_elem:
            desc_elem = soup.find('div', class_='description__text')
        
        text = desc_elem.get_text('\n', strip=True) if desc_elem else ""
        
        return {
            'text': text,
            'title': title,
            'company': company,
            'url': url,
            'source': 'LinkedIn'
        }
    
    def _scrape_indeed(self, url: str) -> Dict[str, Any]:
        """Extract job ad from Indeed."""
        soup = self._fetch_page(url)
        
        # Extract title
        title_elem = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
        if not title_elem:
            title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else "Unknown Position"
        
        # Extract company
        company_elem = soup.find('div', {'data-company-name': True})
        if not company_elem:
            company_elem = soup.find('div', class_='jobsearch-InlineCompanyRating')
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        
        # Extract description
        desc_elem = soup.find('div', id='jobDescriptionText')
        if not desc_elem:
            desc_elem = soup.find('div', class_='jobsearch-jobDescriptionText')
        
        text = desc_elem.get_text('\n', strip=True) if desc_elem else ""
        
        return {
            'text': text,
            'title': title,
            'company': company,
            'url': url,
            'source': 'Indeed'
        }
    
    def _scrape_glassdoor(self, url: str) -> Dict[str, Any]:
        """Extract job ad from Glassdoor."""
        soup = self._fetch_page(url)
        
        # Extract title
        title_elem = soup.find('div', {'data-test': 'job-title'})
        if not title_elem:
            title_elem = soup.find('h1')
        title = title_elem.get_text(strip=True) if title_elem else "Unknown Position"
        
        # Extract company
        company_elem = soup.find('div', {'data-test': 'employer-name'})
        company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
        
        # Extract description
        desc_elem = soup.find('div', class_='jobDescriptionContent')
        if not desc_elem:
            desc_elem = soup.find('div', {'data-test': 'job-description'})
        
        text = desc_elem.get_text('\n', strip=True) if desc_elem else ""
        
        return {
            'text': text,
            'title': title,
            'company': company,
            'url': url,
            'source': 'Glassdoor'
        }
    
    def _scrape_generic(self, url: str) -> Dict[str, Any]:
        """
        Extract job ad from generic website.
        
        Uses heuristics to find job description content.
        """
        soup = self._fetch_page(url)
        
        # Try to find title
        title = "Unknown Position"
        for tag in ['h1', 'h2']:
            title_elem = soup.find(tag)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        # Try to find company
        company = "Unknown Company"
        company_elem = soup.find(text=re.compile(r'company', re.I))
        if company_elem:
            company = company_elem.strip()
        
        # Extract main content
        # Remove script, style, nav, footer
        for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
            tag.decompose()
        
        # Try common job description containers
        desc_elem = None
        for class_hint in ['job-description', 'description', 'content', 'job-details']:
            desc_elem = soup.find('div', class_=re.compile(class_hint, re.I))
            if desc_elem:
                break
        
        if not desc_elem:
            # Fallback: get main or article content
            desc_elem = soup.find('main') or soup.find('article') or soup.find('body')
        
        text = desc_elem.get_text('\n', strip=True) if desc_elem else ""
        
        # Clean up excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return {
            'text': text,
            'title': title,
            'company': company,
            'url': url,
            'source': 'Generic'
        }
    
    def scrape_multiple(self, urls: list[str]) -> list[Dict[str, Any]]:
        """
        Scrape multiple URLs.
        
        Args:
            urls: List of job posting URLs.
            
        Returns:
            List of scraped job ad dictionaries.
        """
        results = []
        for url in urls:
            try:
                result = self.scrape(url)
                results.append(result)
            except Exception as e:
                results.append({
                    'text': '',
                    'title': 'Error',
                    'company': 'Error',
                    'url': url,
                    'source': 'Error',
                    'error': str(e)
                })
        return results
    
    def search_jobs(self, query: str, source: str = "indeed", location: str = "", 
                    max_results: int = 10) -> list[Dict[str, Any]]:
        """
        Search for jobs on a job board and return multiple job ads.
        
        Args:
            query: Search query (e.g., "software engineer", "data analyst").
            source: Job board to search ("indeed", "linkedin", "glassdoor").
            location: Location filter (e.g., "New York, NY", "Remote").
            max_results: Maximum number of results to return (default: 10).
            
        Returns:
            List of job ad dictionaries with text, title, company, url, source.
        """
        source = source.lower()
        
        if source == "indeed":
            return self._search_indeed(query, location, max_results)
        elif source == "linkedin":
            return self._search_linkedin(query, location, max_results)
        elif source == "glassdoor":
            return self._search_glassdoor(query, location, max_results)
        else:
            raise ValueError(f"Unsupported job board: {source}. Use 'indeed', 'linkedin', or 'glassdoor'")
    
    def _search_indeed(self, query: str, location: str, max_results: int) -> list[Dict[str, Any]]:
        """Search Indeed for job listings."""
        # Build search URL
        base_url = "https://www.indeed.com/jobs"
        params = {'q': query}
        if location:
            params['l'] = location
        
        try:
            response = self.session.get(base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_=re.compile('job_seen_beacon', re.I), limit=max_results)
            
            results = []
            for card in job_cards:
                try:
                    # Extract job link
                    link_elem = card.find('a', class_=re.compile('jcs-JobTitle', re.I))
                    if not link_elem:
                        continue
                    
                    job_id = link_elem.get('data-jk', '')
                    if job_id:
                        job_url = f"https://www.indeed.com/viewjob?jk={job_id}"
                    else:
                        href = link_elem.get('href', '')
                        job_url = f"https://www.indeed.com{href}" if href.startswith('/') else href
                    
                    # Extract title
                    title = link_elem.get_text(strip=True)
                    
                    # Extract company
                    company_elem = card.find('span', {'data-testid': 'company-name'})
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    # Scrape full job description
                    job_data = self.scrape(job_url)
                    results.append(job_data)
                    
                except Exception as e:
                    continue
                    
            return results[:max_results]
            
        except Exception as e:
            raise ValueError(f"Failed to search Indeed: {str(e)}")
    
    def _search_linkedin(self, query: str, location: str, max_results: int) -> list[Dict[str, Any]]:
        """Search LinkedIn for job listings."""
        # Build search URL
        base_url = "https://www.linkedin.com/jobs/search/"
        params = {'keywords': query}
        if location:
            params['location'] = location
        
        try:
            response = self.session.get(base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job cards (LinkedIn structure)
            job_cards = soup.find_all('div', class_=re.compile('base-card', re.I), limit=max_results * 2)
            
            results = []
            for card in job_cards:
                if len(results) >= max_results:
                    break
                    
                try:
                    # Extract job link
                    link_elem = card.find('a', class_=re.compile('base-card__full-link', re.I))
                    if not link_elem:
                        continue
                    
                    job_url = link_elem.get('href', '').split('?')[0]  # Remove query params
                    if not job_url.startswith('http'):
                        continue
                    
                    # Extract title
                    title_elem = card.find('h3', class_=re.compile('base-search-card__title', re.I))
                    title = title_elem.get_text(strip=True) if title_elem else "Unknown"
                    
                    # Extract company
                    company_elem = card.find('h4', class_=re.compile('base-search-card__subtitle', re.I))
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                    
                    # Scrape full job description
                    job_data = self.scrape(job_url)
                    results.append(job_data)
                    
                except Exception as e:
                    continue
            
            return results
            
        except Exception as e:
            raise ValueError(f"Failed to search LinkedIn: {str(e)}")
    
    def _search_glassdoor(self, query: str, location: str, max_results: int) -> list[Dict[str, Any]]:
        """Search Glassdoor for job listings."""
        # Build search URL
        base_url = "https://www.glassdoor.com/Job/jobs.htm"
        params = {'sc.keyword': query}
        if location:
            params['locT'] = 'C'
            params['locId'] = location
        
        try:
            response = self.session.get(base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('li', class_=re.compile('react-job-listing', re.I), limit=max_results)
            
            results = []
            for card in job_cards:
                try:
                    # Extract job link
                    link_elem = card.find('a', class_=re.compile('job-search-key', re.I))
                    if not link_elem:
                        continue
                    
                    href = link_elem.get('href', '')
                    job_url = f"https://www.glassdoor.com{href}" if href.startswith('/') else href
                    
                    # Scrape full job description
                    job_data = self.scrape(job_url)
                    results.append(job_data)
                    
                except Exception as e:
                    continue
            
            return results[:max_results]
            
        except Exception as e:
            raise ValueError(f"Failed to search Glassdoor: {str(e)}")
