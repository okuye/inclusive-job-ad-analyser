"""
Tests for web scraping functionality.
"""

import pytest
from unittest.mock import Mock, patch

try:
    from inclusive_job_ad_analyser.scraper import JobAdScraper
    _HAS_SCRAPING = True
except ImportError:
    _HAS_SCRAPING = False


@pytest.mark.skipif(not _HAS_SCRAPING, reason="Scraping dependencies not installed")
class TestJobAdScraper:
    """Tests for JobAdScraper class."""
    
    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing."""
        return JobAdScraper(timeout=5)
    
    @pytest.fixture
    def mock_linkedin_html(self):
        """Mock LinkedIn page HTML."""
        return """
        <html>
            <h1 class="top-card-layout__title">Senior Software Engineer</h1>
            <a class="topcard__org-name-link">Tech Company</a>
            <div class="show-more-less-html__markup">
                <p>We're looking for a skilled professional to join our team.</p>
                <p>Requirements: 3+ years experience</p>
            </div>
        </html>
        """
    
    @pytest.fixture
    def mock_indeed_html(self):
        """Mock Indeed page HTML."""
        return """
        <html>
            <h1 class="jobsearch-JobInfoHeader-title">Data Scientist</h1>
            <div data-company-name="true">Analytics Corp</div>
            <div id="jobDescriptionText">
                <p>Join our data science team</p>
                <p>Must have Python and SQL skills</p>
            </div>
        </html>
        """
    
    def test_scraper_initializes(self, scraper):
        """Test that scraper initializes correctly."""
        assert scraper is not None
        assert scraper.timeout == 5
        assert scraper.session is not None
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_scrape_linkedin(self, mock_get, scraper, mock_linkedin_html):
        """Test scraping LinkedIn job ad."""
        # Mock response
        mock_response = Mock()
        mock_response.text = mock_linkedin_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        url = "https://www.linkedin.com/jobs/view/123456"
        result = scraper.scrape(url)
        
        assert result['source'] == 'LinkedIn'
        assert result['title'] == 'Senior Software Engineer'
        assert result['company'] == 'Tech Company'
        assert 'skilled professional' in result['text']
        assert result['url'] == url
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_scrape_indeed(self, mock_get, scraper, mock_indeed_html):
        """Test scraping Indeed job ad."""
        # Mock response
        mock_response = Mock()
        mock_response.text = mock_indeed_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        url = "https://www.indeed.com/viewjob?jk=abc123"
        result = scraper.scrape(url)
        
        assert result['source'] == 'Indeed'
        assert result['title'] == 'Data Scientist'
        assert result['company'] == 'Analytics Corp'
        assert 'Python' in result['text']
        assert result['url'] == url
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_scrape_generic(self, mock_get, scraper):
        """Test scraping generic website."""
        html = """
        <html>
            <body>
                <h1>Product Manager</h1>
                <div class="job-description">
                    <p>Lead product development</p>
                </div>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        url = "https://example.com/careers/product-manager"
        result = scraper.scrape(url)
        
        assert result['source'] == 'Generic'
        assert result['title'] == 'Product Manager'
        assert 'product development' in result['text'].lower()
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_scrape_handles_errors(self, mock_get, scraper):
        """Test error handling during scraping."""
        import requests
        mock_get.side_effect = requests.RequestException("Connection error")
        
        with pytest.raises(ValueError, match="Failed to fetch URL"):
            scraper.scrape("https://example.com/job")
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_scrape_multiple(self, mock_get, scraper, mock_linkedin_html):
        """Test scraping multiple URLs."""
        mock_response = Mock()
        mock_response.text = mock_linkedin_html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        urls = [
            "https://www.linkedin.com/jobs/view/123",
            "https://www.linkedin.com/jobs/view/456"
        ]
        
        results = scraper.scrape_multiple(urls)
        
        assert len(results) == 2
        assert all(r['source'] == 'LinkedIn' for r in results)
    
    def test_scraper_requires_dependencies(self):
        """Test that scraper requires optional dependencies."""
        # This test verifies the import check works
        assert _HAS_SCRAPING is True
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_search_indeed(self, mock_get, scraper):
        """Test searching Indeed for jobs."""
        # Mock search results page
        search_html = """
        <html>
            <div class="job_seen_beacon">
                <a class="jcs-JobTitle" data-jk="job123">Software Engineer</a>
                <span data-testid="company-name">Tech Corp</span>
            </div>
            <div class="job_seen_beacon">
                <a class="jcs-JobTitle" data-jk="job456">Senior Developer</a>
                <span data-testid="company-name">StartupCo</span>
            </div>
        </html>
        """
        
        # Mock job detail page
        job_html = """
        <html>
            <h1 class="jobsearch-JobInfoHeader-title">Software Engineer</h1>
            <div data-company-name="true">Tech Corp</div>
            <div id="jobDescriptionText">
                <p>We are looking for a talented software engineer</p>
            </div>
        </html>
        """
        
        def mock_response(*args, **kwargs):
            response = Mock()
            if 'viewjob' in str(args):
                response.text = job_html
            else:
                response.text = search_html
            response.raise_for_status = Mock()
            return response
        
        mock_get.side_effect = mock_response
        
        results = scraper.search_jobs("software engineer", source="indeed", max_results=2)
        
        assert len(results) <= 2
        assert all('text' in job for job in results)
    
    @patch('inclusive_job_ad_analyser.scraper.requests.Session.get')
    def test_search_linkedin(self, mock_get, scraper):
        """Test searching LinkedIn for jobs."""
        search_html = """
        <html>
            <div class="base-card">
                <a class="base-card__full-link" href="https://www.linkedin.com/jobs/view/123">Link</a>
                <h3 class="base-search-card__title">Product Manager</h3>
                <h4 class="base-search-card__subtitle">Tech Company</h4>
            </div>
        </html>
        """
        
        job_html = """
        <html>
            <h1 class="top-card-layout__title">Product Manager</h1>
            <a class="topcard__org-name-link">Tech Company</a>
            <div class="show-more-less-html__markup">
                <p>Join our product team</p>
            </div>
        </html>
        """
        
        def mock_response(*args, **kwargs):
            response = Mock()
            if '/jobs/view/' in str(args):
                response.text = job_html
            else:
                response.text = search_html
            response.raise_for_status = Mock()
            return response
        
        mock_get.side_effect = mock_response
        
        results = scraper.search_jobs("product manager", source="linkedin", max_results=5)
        
        assert isinstance(results, list)
    
    def test_search_invalid_source(self, scraper):
        """Test that invalid source raises error."""
        with pytest.raises(ValueError, match="Unsupported job board"):
            scraper.search_jobs("test", source="invalid")

