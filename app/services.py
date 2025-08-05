from typing import List, Optional
from datetime import datetime
from sqlmodel import select, desc, and_
from app.database import get_session
from app.models import (
    User,
    Project,
    ProjectImage,
    Gallery,
    Photo,
    ThreeDProject,
    ThreeDRender,
    ContactMessage,
    SiteConfig,
    ProjectType,
    ProjectStatus,
    GalleryType,
    MessageStatus,
    ContactMessageCreate,
)


class PortfolioService:
    """Service layer for portfolio data operations."""

    @staticmethod
    def get_site_config() -> Optional[SiteConfig]:
        """Get site configuration."""
        with get_session() as session:
            return session.exec(select(SiteConfig)).first()

    @staticmethod
    def get_portfolio_owner() -> Optional[User]:
        """Get the portfolio owner (first active user)."""
        with get_session() as session:
            return session.exec(select(User).where(User.is_active)).first()

    @staticmethod
    def get_featured_projects(limit: int = 6) -> List[Project]:
        """Get featured projects for homepage showcase."""
        with get_session() as session:
            return list(
                session.exec(
                    select(Project)
                    .where(and_(Project.status == ProjectStatus.PUBLISHED, Project.featured))
                    .order_by(desc(Project.sort_order), desc(Project.created_at))
                    .limit(limit)
                )
            )

    @staticmethod
    def get_projects_by_type(project_type: ProjectType, limit: Optional[int] = None) -> List[Project]:
        """Get projects filtered by type."""
        with get_session() as session:
            query = (
                select(Project)
                .where(and_(Project.status == ProjectStatus.PUBLISHED, Project.project_type == project_type))
                .order_by(desc(Project.sort_order), desc(Project.created_at))
            )

            if limit:
                query = query.limit(limit)

            return list(session.exec(query))

    @staticmethod
    def get_project_by_slug(slug: str) -> Optional[Project]:
        """Get a project by its slug."""
        with get_session() as session:
            project = session.exec(select(Project).where(Project.slug == slug)).first()
            if project:
                # Increment view count
                project.view_count += 1
                session.add(project)
                session.commit()
                session.refresh(project)
            return project

    @staticmethod
    def get_project_images(project_id: int) -> List[ProjectImage]:
        """Get images for a project."""
        with get_session() as session:
            return list(session.exec(select(ProjectImage).where(ProjectImage.project_id == project_id)))

    @staticmethod
    def get_featured_galleries(limit: int = 6) -> List[Gallery]:
        """Get featured photography galleries."""
        with get_session() as session:
            return list(
                session.exec(
                    select(Gallery)
                    .where(and_(Gallery.is_public, Gallery.featured))
                    .order_by(desc(Gallery.sort_order), desc(Gallery.created_at))
                    .limit(limit)
                )
            )

    @staticmethod
    def get_galleries_by_type(gallery_type: GalleryType, limit: Optional[int] = None) -> List[Gallery]:
        """Get galleries filtered by type."""
        with get_session() as session:
            query = (
                select(Gallery)
                .where(and_(Gallery.is_public, Gallery.gallery_type == gallery_type))
                .order_by(desc(Gallery.sort_order), desc(Gallery.created_at))
            )

            if limit:
                query = query.limit(limit)

            return list(session.exec(query))

    @staticmethod
    def get_gallery_by_slug(slug: str) -> Optional[Gallery]:
        """Get a gallery by its slug."""
        with get_session() as session:
            gallery = session.exec(select(Gallery).where(Gallery.slug == slug)).first()
            if gallery:
                # Increment view count
                gallery.view_count += 1
                session.add(gallery)
                session.commit()
                session.refresh(gallery)
            return gallery

    @staticmethod
    def get_gallery_photos(gallery_id: int) -> List[Photo]:
        """Get photos for a gallery."""
        with get_session() as session:
            return list(session.exec(select(Photo).where(Photo.gallery_id == gallery_id)))

    @staticmethod
    def get_featured_3d_projects(limit: int = 6) -> List[ThreeDProject]:
        """Get featured 3D design projects."""
        with get_session() as session:
            return list(
                session.exec(
                    select(ThreeDProject)
                    .where(ThreeDProject.featured)
                    .order_by(desc(ThreeDProject.sort_order), desc(ThreeDProject.created_at))
                    .limit(limit)
                )
            )

    @staticmethod
    def get_3d_project_by_slug(slug: str) -> Optional[ThreeDProject]:
        """Get a 3D project by its slug."""
        with get_session() as session:
            project = session.exec(select(ThreeDProject).where(ThreeDProject.slug == slug)).first()
            if project:
                # Increment view count
                project.view_count += 1
                session.add(project)
                session.commit()
                session.refresh(project)
            return project

    @staticmethod
    def get_3d_project_renders(project_id: int) -> List[ThreeDRender]:
        """Get renders for a 3D project."""
        with get_session() as session:
            return list(session.exec(select(ThreeDRender).where(ThreeDRender.project_id == project_id)))

    @staticmethod
    def create_contact_message(
        message_data: ContactMessageCreate, ip_address: str = "", user_agent: str = ""
    ) -> ContactMessage:
        """Create a new contact message."""
        with get_session() as session:
            message = ContactMessage(
                name=message_data.name,
                email=message_data.email,
                subject=message_data.subject,
                message=message_data.message,
                ip_address=ip_address,
                user_agent=user_agent,
                status=MessageStatus.NEW,
                created_at=datetime.utcnow(),
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message

    @staticmethod
    def get_recent_messages(limit: int = 10) -> List[ContactMessage]:
        """Get recent contact messages."""
        with get_session() as session:
            return list(session.exec(select(ContactMessage).order_by(desc(ContactMessage.created_at)).limit(limit)))


class SeedDataService:
    """Service for seeding initial portfolio data."""

    @staticmethod
    def create_sample_data():
        """Create sample portfolio data for demonstration."""
        with get_session() as session:
            # Check if data already exists
            existing_user = session.exec(select(User)).first()
            if existing_user:
                return  # Data already seeded

            # Create portfolio owner
            owner = User(
                name="Alexandra Smith",
                email="alex@portfolio.com",
                bio="I'm a passionate UI/UX designer and photographer with over 5 years of experience creating meaningful digital experiences and capturing life's beautiful moments.",
                profession="UI/UX Designer & Photographer",
                location="San Francisco, CA",
                website="https://alexandra-portfolio.com",
                linkedin="https://linkedin.com/in/alexandrasmith",
                instagram="https://instagram.com/alex_designs",
                behance="https://behance.net/alexandrasmith",
                dribbble="https://dribbble.com/alexsmith",
            )
            session.add(owner)
            session.commit()
            session.refresh(owner)

            # Create site configuration
            site_config = SiteConfig(
                site_title="Alexandra Smith - Designer & Photographer",
                site_description="Portfolio showcasing UI/UX design work, photography, and 3D renders",
                owner_name="Alexandra Smith",
                hero_title="Creating Digital Experiences & Capturing Moments",
                hero_subtitle="UI/UX Designer & Photographer passionate about storytelling through design and photography",
                hero_image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
                about_text="I believe great design should be both beautiful and functional. With a background in both digital design and photography, I bring a unique perspective to every project.",
                about_image_url="https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop",
                contact_email="hello@alexandra-portfolio.com",
                social_links={
                    "linkedin": "https://linkedin.com/in/alexandrasmith",
                    "instagram": "https://instagram.com/alex_designs",
                    "behance": "https://behance.net/alexandrasmith",
                    "dribbble": "https://dribbble.com/alexsmith",
                },
                theme_colors={"primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
            )
            session.add(site_config)

            # Create sample UI/UX projects
            projects = [
                Project(
                    title="EcoShop Mobile App",
                    slug="ecoshop-mobile-app",
                    description="A sustainable shopping app that helps users make eco-friendly choices",
                    detailed_description="EcoShop is a mobile application designed to promote sustainable shopping habits. The app features product sustainability ratings, carbon footprint tracking, and personalized recommendations for eco-friendly alternatives.",
                    project_type=ProjectType.UI_UX,
                    status=ProjectStatus.PUBLISHED,
                    thumbnail_url="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300&fit=crop",
                    cover_image_url="https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=800&h=600&fit=crop",
                    client_name="EcoTech Solutions",
                    tags=["Mobile App", "UI/UX", "Sustainability", "E-commerce"],
                    technologies=["Figma", "Sketch", "Principle", "InVision"],
                    color_palette=["#22C55E", "#16A34A", "#FFFFFF", "#F3F4F6"],
                    project_duration="3 months",
                    featured=True,
                    sort_order=1,
                    owner_id=owner.id if owner.id else 1,
                ),
                Project(
                    title="MindfulSpace Dashboard",
                    slug="mindfulspace-dashboard",
                    description="A wellness platform dashboard for meditation and mindfulness tracking",
                    detailed_description="MindfulSpace is a comprehensive wellness platform that helps users track their meditation progress, set mindfulness goals, and connect with guided sessions. The dashboard provides clear analytics and a calming user experience.",
                    project_type=ProjectType.UI_UX,
                    status=ProjectStatus.PUBLISHED,
                    thumbnail_url="https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=400&h=300&fit=crop",
                    cover_image_url="https://images.unsplash.com/photo-1544717297-fa95b6ee9643?w=800&h=600&fit=crop",
                    client_name="Wellness Tech Inc",
                    tags=["Web App", "Dashboard", "Wellness", "Analytics"],
                    technologies=["Figma", "React", "Chart.js", "Framer Motion"],
                    color_palette=["#8B5CF6", "#A78BFA", "#F3F4F6", "#FFFFFF"],
                    project_duration="2 months",
                    featured=True,
                    sort_order=2,
                    owner_id=owner.id if owner.id else 1,
                ),
            ]

            for project in projects:
                session.add(project)

            session.commit()

            # Create sample photography galleries
            galleries = [
                Gallery(
                    title="Urban Landscapes",
                    slug="urban-landscapes",
                    description="Capturing the beauty and energy of city life through architectural photography",
                    gallery_type=GalleryType.PORTFOLIO,
                    cover_image_url="https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop",
                    location="San Francisco, CA",
                    featured=True,
                    sort_order=1,
                    owner_id=owner.id if owner.id else 1,
                ),
                Gallery(
                    title="Portrait Sessions",
                    slug="portrait-sessions",
                    description="Professional portraits that capture personality and emotion",
                    gallery_type=GalleryType.CLIENT,
                    cover_image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop",
                    location="Studio & On-location",
                    featured=True,
                    sort_order=2,
                    owner_id=owner.id if owner.id else 1,
                ),
            ]

            for gallery in galleries:
                session.add(gallery)

            session.commit()

            # Create sample 3D projects
            three_d_projects = [
                ThreeDProject(
                    title="Modern Living Room",
                    slug="modern-living-room",
                    description="Architectural visualization of a contemporary living space",
                    software_used=["Blender", "Cycles"],
                    render_engine="Cycles",
                    render_time="45 minutes",
                    polygon_count=250000,
                    texture_resolution="4K",
                    featured_image_url="https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&h=600&fit=crop",
                    project_type="Interior Design",
                    style="Photorealistic",
                    tags=["Architecture", "Interior", "Visualization"],
                    featured=True,
                    sort_order=1,
                ),
                ThreeDProject(
                    title="Abstract Composition",
                    slug="abstract-composition",
                    description="Experimental 3D artwork exploring form and color",
                    software_used=["Cinema 4D", "Octane"],
                    render_engine="Octane",
                    render_time="20 minutes",
                    polygon_count=150000,
                    texture_resolution="2K",
                    featured_image_url="https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&h=600&fit=crop",
                    project_type="Abstract Art",
                    style="Stylized",
                    tags=["Abstract", "Art", "Experimental"],
                    featured=True,
                    sort_order=2,
                ),
            ]

            for project in three_d_projects:
                session.add(project)

            session.commit()
