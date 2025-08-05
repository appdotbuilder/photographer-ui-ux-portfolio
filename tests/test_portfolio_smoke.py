import pytest
from app.services import PortfolioService, SeedDataService
from app.database import reset_db


@pytest.fixture
def new_db():
    reset_db()
    yield
    reset_db()


def test_portfolio_service_integration(new_db):
    """Test that portfolio services work with seeded data."""
    SeedDataService.create_sample_data()

    # Test site config
    config = PortfolioService.get_site_config()
    assert config is not None
    assert config.site_title == "Alexandra Smith - Designer & Photographer"

    # Test owner
    owner = PortfolioService.get_portfolio_owner()
    assert owner is not None
    assert owner.name == "Alexandra Smith"

    # Test featured projects
    projects = PortfolioService.get_featured_projects()
    assert len(projects) >= 1
    assert all(project.featured for project in projects)

    # Test galleries
    galleries = PortfolioService.get_featured_galleries()
    assert len(galleries) >= 1
    assert all(gallery.featured for gallery in galleries)

    # Test 3D projects
    three_d_projects = PortfolioService.get_featured_3d_projects()
    assert len(three_d_projects) >= 1
    assert all(project.featured for project in three_d_projects)


def test_portfolio_project_slugs(new_db):
    """Test that project slugs work correctly."""
    SeedDataService.create_sample_data()

    # Test UI/UX project
    project = PortfolioService.get_project_by_slug("ecoshop-mobile-app")
    assert project is not None
    assert project.title == "EcoShop Mobile App"
    assert project.project_type.value == "ui_ux"

    # Test gallery
    gallery = PortfolioService.get_gallery_by_slug("urban-landscapes")
    assert gallery is not None
    assert gallery.title == "Urban Landscapes"

    # Test 3D project
    three_d_project = PortfolioService.get_3d_project_by_slug("modern-living-room")
    assert three_d_project is not None
    assert three_d_project.title == "Modern Living Room"


def test_contact_message_flow(new_db):
    """Test complete contact message flow."""
    from app.models import ContactMessageCreate

    # Create message
    message_data = ContactMessageCreate(
        name="Test User",
        email="test@example.com",
        subject="Portfolio Inquiry",
        message="I love your work! Let's connect.",
    )

    message = PortfolioService.create_contact_message(message_data)
    assert message.id is not None
    assert message.name == "Test User"
    assert message.email == "test@example.com"

    # Verify message appears in recent messages
    recent_messages = PortfolioService.get_recent_messages()
    assert len(recent_messages) >= 1
    assert any(msg.email == "test@example.com" for msg in recent_messages)


def test_project_view_counts(new_db):
    """Test that view counts increment correctly."""
    SeedDataService.create_sample_data()

    # Get initial view count
    project = PortfolioService.get_project_by_slug("ecoshop-mobile-app")
    initial_count = project.view_count if project else 0

    # View project again (should increment)
    project_again = PortfolioService.get_project_by_slug("ecoshop-mobile-app")
    assert project_again is not None
    assert project_again.view_count > initial_count

    # Test gallery view count
    gallery = PortfolioService.get_gallery_by_slug("urban-landscapes")
    initial_gallery_count = gallery.view_count if gallery else 0

    gallery_again = PortfolioService.get_gallery_by_slug("urban-landscapes")
    assert gallery_again is not None
    assert gallery_again.view_count > initial_gallery_count


def test_portfolio_data_structure(new_db):
    """Test that seeded data has proper structure."""
    SeedDataService.create_sample_data()

    # Test project has required fields
    projects = PortfolioService.get_featured_projects()
    for project in projects:
        assert project.title
        assert project.slug
        assert project.description
        assert project.project_type
        assert project.status
        assert project.owner_id
        assert project.created_at

    # Test gallery has required fields
    galleries = PortfolioService.get_featured_galleries()
    for gallery in galleries:
        assert gallery.title
        assert gallery.slug
        assert gallery.gallery_type
        assert gallery.owner_id
        assert gallery.created_at

    # Test 3D project has required fields
    three_d_projects = PortfolioService.get_featured_3d_projects()
    for project in three_d_projects:
        assert project.title
        assert project.slug
        assert project.description
        assert project.created_at
