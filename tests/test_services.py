import pytest
from app.services import PortfolioService, SeedDataService
from app.models import ContactMessageCreate, ProjectType, GalleryType, MessageStatus
from app.database import reset_db


@pytest.fixture
def new_db():
    reset_db()
    yield
    reset_db()


def test_seed_data_creation(new_db):
    """Test that sample data is created correctly."""
    SeedDataService.create_sample_data()

    # Test site config exists
    config = PortfolioService.get_site_config()
    assert config is not None
    assert config.site_title == "Alexandra Smith - Designer & Photographer"
    assert "Creating Digital Experiences" in config.hero_title

    # Test owner exists
    owner = PortfolioService.get_portfolio_owner()
    assert owner is not None
    assert owner.name == "Alexandra Smith"
    assert owner.profession == "UI/UX Designer & Photographer"


def test_get_featured_projects(new_db):
    """Test fetching featured projects."""
    SeedDataService.create_sample_data()

    projects = PortfolioService.get_featured_projects()
    assert len(projects) >= 1

    # All should be featured and published
    for project in projects:
        assert project.featured
        assert project.status.value == "published"


def test_get_projects_by_type(new_db):
    """Test filtering projects by type."""
    SeedDataService.create_sample_data()

    ui_ux_projects = PortfolioService.get_projects_by_type(ProjectType.UI_UX)
    assert len(ui_ux_projects) >= 1

    for project in ui_ux_projects:
        assert project.project_type == ProjectType.UI_UX


def test_get_project_by_slug(new_db):
    """Test fetching project by slug and view count increment."""
    SeedDataService.create_sample_data()

    project = PortfolioService.get_project_by_slug("ecoshop-mobile-app")
    assert project is not None
    assert project.title == "EcoShop Mobile App"
    assert project.view_count == 1

    # Test view count increment
    project_again = PortfolioService.get_project_by_slug("ecoshop-mobile-app")
    assert project_again is not None
    assert project_again.view_count == 2


def test_get_project_by_nonexistent_slug(new_db):
    """Test fetching project with non-existent slug returns None."""
    SeedDataService.create_sample_data()

    project = PortfolioService.get_project_by_slug("nonexistent-project")
    assert project is None


def test_get_featured_galleries(new_db):
    """Test fetching featured galleries."""
    SeedDataService.create_sample_data()

    galleries = PortfolioService.get_featured_galleries()
    assert len(galleries) >= 1

    for gallery in galleries:
        assert gallery.featured
        assert gallery.is_public


def test_get_galleries_by_type(new_db):
    """Test filtering galleries by type."""
    SeedDataService.create_sample_data()

    portfolio_galleries = PortfolioService.get_galleries_by_type(GalleryType.PORTFOLIO)
    assert len(portfolio_galleries) >= 1

    for gallery in portfolio_galleries:
        assert gallery.gallery_type == GalleryType.PORTFOLIO


def test_get_gallery_by_slug(new_db):
    """Test fetching gallery by slug and view count increment."""
    SeedDataService.create_sample_data()

    gallery = PortfolioService.get_gallery_by_slug("urban-landscapes")
    assert gallery is not None
    assert gallery.title == "Urban Landscapes"
    assert gallery.view_count == 1

    # Test view count increment
    gallery_again = PortfolioService.get_gallery_by_slug("urban-landscapes")
    assert gallery_again is not None
    assert gallery_again.view_count == 2


def test_get_gallery_by_nonexistent_slug(new_db):
    """Test fetching gallery with non-existent slug returns None."""
    SeedDataService.create_sample_data()

    gallery = PortfolioService.get_gallery_by_slug("nonexistent-gallery")
    assert gallery is None


def test_get_featured_3d_projects(new_db):
    """Test fetching featured 3D projects."""
    SeedDataService.create_sample_data()

    projects = PortfolioService.get_featured_3d_projects()
    assert len(projects) >= 1

    for project in projects:
        assert project.featured


def test_get_3d_project_by_slug(new_db):
    """Test fetching 3D project by slug and view count increment."""
    SeedDataService.create_sample_data()

    project = PortfolioService.get_3d_project_by_slug("modern-living-room")
    assert project is not None
    assert project.title == "Modern Living Room"
    assert project.view_count == 1

    # Test view count increment
    project_again = PortfolioService.get_3d_project_by_slug("modern-living-room")
    assert project_again is not None
    assert project_again.view_count == 2


def test_get_3d_project_by_nonexistent_slug(new_db):
    """Test fetching 3D project with non-existent slug returns None."""
    SeedDataService.create_sample_data()

    project = PortfolioService.get_3d_project_by_slug("nonexistent-3d-project")
    assert project is None


def test_create_contact_message(new_db):
    """Test creating a contact message."""
    message_data = ContactMessageCreate(
        name="John Doe",
        email="john@example.com",
        subject="Project Inquiry",
        message="I would like to discuss a potential project.",
    )

    message = PortfolioService.create_contact_message(message_data, ip_address="192.168.1.1", user_agent="Test Browser")

    assert message.id is not None
    assert message.name == "John Doe"
    assert message.email == "john@example.com"
    assert message.subject == "Project Inquiry"
    assert message.status == MessageStatus.NEW
    assert message.ip_address == "192.168.1.1"
    assert message.user_agent == "Test Browser"
    assert message.created_at is not None


def test_get_recent_messages(new_db):
    """Test fetching recent contact messages."""
    # Create some test messages
    for i in range(3):
        message_data = ContactMessageCreate(
            name=f"User {i}", email=f"user{i}@example.com", subject=f"Subject {i}", message=f"Message content {i}"
        )
        PortfolioService.create_contact_message(message_data)

    messages = PortfolioService.get_recent_messages(limit=2)
    assert len(messages) == 2

    # Should be ordered by most recent first
    assert messages[0].name == "User 2"
    assert messages[1].name == "User 1"


def test_get_project_images_empty(new_db):
    """Test getting images for non-existent project returns empty list."""
    images = PortfolioService.get_project_images(999)
    assert images == []


def test_get_gallery_photos_empty(new_db):
    """Test getting photos for non-existent gallery returns empty list."""
    photos = PortfolioService.get_gallery_photos(999)
    assert photos == []


def test_get_3d_project_renders_empty(new_db):
    """Test getting renders for non-existent 3D project returns empty list."""
    renders = PortfolioService.get_3d_project_renders(999)
    assert renders == []


def test_duplicate_seed_data_creation(new_db):
    """Test that creating seed data twice doesn't create duplicates."""
    SeedDataService.create_sample_data()
    SeedDataService.create_sample_data()  # Should not create duplicates

    # Should still have only one owner
    owner = PortfolioService.get_portfolio_owner()
    assert owner is not None
    assert owner.name == "Alexandra Smith"

    # Should still have sample projects
    projects = PortfolioService.get_featured_projects()
    assert len(projects) >= 1
