from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


# Enums for project types and categories
class ProjectType(str, Enum):
    UI_UX = "ui_ux"
    PHOTOGRAPHY = "photography"
    THREE_D = "3d_design"
    OTHER = "other"


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class MessageStatus(str, Enum):
    NEW = "new"
    READ = "read"
    REPLIED = "replied"
    ARCHIVED = "archived"


class GalleryType(str, Enum):
    PORTFOLIO = "portfolio"
    PERSONAL = "personal"
    CLIENT = "client"
    EXHIBITION = "exhibition"


# User/Admin model for portfolio owner
class User(SQLModel, table=True):
    __tablename__ = "users"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(unique=True, max_length=255)
    bio: str = Field(default="", max_length=2000)
    profession: str = Field(default="", max_length=100)
    location: str = Field(default="", max_length=100)
    website: str = Field(default="", max_length=255)
    linkedin: str = Field(default="", max_length=255)
    instagram: str = Field(default="", max_length=255)
    behance: str = Field(default="", max_length=255)
    dribbble: str = Field(default="", max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    projects: List["Project"] = Relationship(back_populates="owner")
    galleries: List["Gallery"] = Relationship(back_populates="owner")


# Project model for UI/UX case studies and general projects
class Project(SQLModel, table=True):
    __tablename__ = "projects"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    description: str = Field(default="", max_length=1000)
    detailed_description: str = Field(default="", max_length=5000)
    project_type: ProjectType = Field(default=ProjectType.OTHER)
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT)
    thumbnail_url: str = Field(default="", max_length=500)
    cover_image_url: str = Field(default="", max_length=500)
    client_name: str = Field(default="", max_length=100)
    project_url: str = Field(default="", max_length=500)
    github_url: str = Field(default="", max_length=500)
    behance_url: str = Field(default="", max_length=500)
    dribbble_url: str = Field(default="", max_length=500)
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    technologies: List[str] = Field(default=[], sa_column=Column(JSON))
    color_palette: List[str] = Field(default=[], sa_column=Column(JSON))
    project_duration: str = Field(default="", max_length=50)
    completion_date: Optional[datetime] = Field(default=None)
    featured: bool = Field(default=False)
    sort_order: int = Field(default=0)
    view_count: int = Field(default=0)
    like_count: int = Field(default=0)
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: User = Relationship(back_populates="projects")
    images: List["ProjectImage"] = Relationship(back_populates="project")
    sections: List["ProjectSection"] = Relationship(back_populates="project")


# Project images for showcasing work
class ProjectImage(SQLModel, table=True):
    __tablename__ = "project_images"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    image_url: str = Field(max_length=500)
    alt_text: str = Field(default="", max_length=200)
    caption: str = Field(default="", max_length=500)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    sort_order: int = Field(default=0)
    is_featured: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: Project = Relationship(back_populates="images")


# Project sections for detailed case studies
class ProjectSection(SQLModel, table=True):
    __tablename__ = "project_sections"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id")
    title: str = Field(max_length=200)
    content: str = Field(max_length=5000)
    section_type: str = Field(default="text", max_length=50)  # text, image, video, code
    image_url: str = Field(default="", max_length=500)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: Project = Relationship(back_populates="sections")


# Gallery model for photography collections
class Gallery(SQLModel, table=True):
    __tablename__ = "galleries"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    description: str = Field(default="", max_length=1000)
    gallery_type: GalleryType = Field(default=GalleryType.PORTFOLIO)
    cover_image_url: str = Field(default="", max_length=500)
    location: str = Field(default="", max_length=100)
    shoot_date: Optional[datetime] = Field(default=None)
    featured: bool = Field(default=False)
    is_public: bool = Field(default=True)
    sort_order: int = Field(default=0)
    view_count: int = Field(default=0)
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    owner: User = Relationship(back_populates="galleries")
    photos: List["Photo"] = Relationship(back_populates="gallery")


# Photo model for individual images in galleries
class Photo(SQLModel, table=True):
    __tablename__ = "photos"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    gallery_id: int = Field(foreign_key="galleries.id")
    title: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=1000)
    image_url: str = Field(max_length=500)
    thumbnail_url: str = Field(default="", max_length=500)
    alt_text: str = Field(default="", max_length=200)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    camera_model: str = Field(default="", max_length=100)
    lens: str = Field(default="", max_length=100)
    focal_length: str = Field(default="", max_length=20)
    aperture: str = Field(default="", max_length=10)
    shutter_speed: str = Field(default="", max_length=20)
    iso: str = Field(default="", max_length=10)
    taken_at: Optional[datetime] = Field(default=None)
    location: str = Field(default="", max_length=100)
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    featured: bool = Field(default=False)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    gallery: Gallery = Relationship(back_populates="photos")


# 3D Design model for static renders
class ThreeDProject(SQLModel, table=True):
    __tablename__ = "three_d_projects"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=200)
    description: str = Field(default="", max_length=1000)
    software_used: List[str] = Field(default=[], sa_column=Column(JSON))  # Blender, Maya, C4D, etc.
    render_engine: str = Field(default="", max_length=50)
    render_time: str = Field(default="", max_length=50)
    polygon_count: Optional[int] = Field(default=None)
    texture_resolution: str = Field(default="", max_length=50)
    featured_image_url: str = Field(default="", max_length=500)
    project_type: str = Field(default="", max_length=50)  # character, environment, product, etc.
    style: str = Field(default="", max_length=50)  # realistic, stylized, abstract, etc.
    tags: List[str] = Field(default=[], sa_column=Column(JSON))
    featured: bool = Field(default=False)
    sort_order: int = Field(default=0)
    view_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    renders: List["ThreeDRender"] = Relationship(back_populates="project")


# 3D Render model for individual renders
class ThreeDRender(SQLModel, table=True):
    __tablename__ = "three_d_renders"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="three_d_projects.id")
    title: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=500)
    image_url: str = Field(max_length=500)
    thumbnail_url: str = Field(default="", max_length=500)
    alt_text: str = Field(default="", max_length=200)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    file_size: Optional[int] = Field(default=None)
    render_settings: Dict[str, Any] = Field(default={}, sa_column=Column(JSON))
    is_final: bool = Field(default=True)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    project: ThreeDProject = Relationship(back_populates="renders")


# Contact message model for contact form submissions
class ContactMessage(SQLModel, table=True):
    __tablename__ = "contact_messages"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)
    subject: str = Field(max_length=200)
    message: str = Field(max_length=2000)
    status: MessageStatus = Field(default=MessageStatus.NEW)
    ip_address: str = Field(default="", max_length=45)
    user_agent: str = Field(default="", max_length=500)
    replied_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Site configuration model for portfolio settings
class SiteConfig(SQLModel, table=True):
    __tablename__ = "site_config"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    site_title: str = Field(default="Portfolio", max_length=100)
    site_description: str = Field(default="", max_length=500)
    owner_name: str = Field(default="", max_length=100)
    hero_title: str = Field(default="", max_length=200)
    hero_subtitle: str = Field(default="", max_length=300)
    hero_image_url: str = Field(default="", max_length=500)
    about_text: str = Field(default="", max_length=2000)
    about_image_url: str = Field(default="", max_length=500)
    contact_email: str = Field(default="", max_length=255)
    phone: str = Field(default="", max_length=20)
    address: str = Field(default="", max_length=200)
    social_links: Dict[str, str] = Field(default={}, sa_column=Column(JSON))
    theme_colors: Dict[str, str] = Field(default={}, sa_column=Column(JSON))
    seo_keywords: List[str] = Field(default=[], sa_column=Column(JSON))
    google_analytics_id: str = Field(default="", max_length=50)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schemas for validation and API


# Contact form schema
class ContactMessageCreate(SQLModel, table=False):
    name: str = Field(max_length=100)
    email: str = Field(max_length=255)
    subject: str = Field(max_length=200)
    message: str = Field(max_length=2000)


class ContactMessageUpdate(SQLModel, table=False):
    status: Optional[MessageStatus] = Field(default=None)
    replied_at: Optional[datetime] = Field(default=None)


# Project schemas
class ProjectCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    detailed_description: str = Field(default="", max_length=5000)
    project_type: ProjectType = Field(default=ProjectType.OTHER)
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT)
    thumbnail_url: str = Field(default="", max_length=500)
    cover_image_url: str = Field(default="", max_length=500)
    client_name: str = Field(default="", max_length=100)
    project_url: str = Field(default="", max_length=500)
    tags: List[str] = Field(default=[])
    technologies: List[str] = Field(default=[])
    color_palette: List[str] = Field(default=[])
    project_duration: str = Field(default="", max_length=50)
    completion_date: Optional[datetime] = Field(default=None)
    featured: bool = Field(default=False)
    owner_id: int


class ProjectUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    detailed_description: Optional[str] = Field(default=None, max_length=5000)
    status: Optional[ProjectStatus] = Field(default=None)
    thumbnail_url: Optional[str] = Field(default=None, max_length=500)
    cover_image_url: Optional[str] = Field(default=None, max_length=500)
    featured: Optional[bool] = Field(default=None)
    tags: Optional[List[str]] = Field(default=None)
    technologies: Optional[List[str]] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Gallery schemas
class GalleryCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    gallery_type: GalleryType = Field(default=GalleryType.PORTFOLIO)
    cover_image_url: str = Field(default="", max_length=500)
    location: str = Field(default="", max_length=100)
    shoot_date: Optional[datetime] = Field(default=None)
    featured: bool = Field(default=False)
    is_public: bool = Field(default=True)
    owner_id: int


class GalleryUpdate(SQLModel, table=False):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    cover_image_url: Optional[str] = Field(default=None, max_length=500)
    featured: Optional[bool] = Field(default=None)
    is_public: Optional[bool] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Photo schemas
class PhotoCreate(SQLModel, table=False):
    gallery_id: int
    title: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=1000)
    image_url: str = Field(max_length=500)
    thumbnail_url: str = Field(default="", max_length=500)
    alt_text: str = Field(default="", max_length=200)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    camera_model: str = Field(default="", max_length=100)
    lens: str = Field(default="", max_length=100)
    focal_length: str = Field(default="", max_length=20)
    aperture: str = Field(default="", max_length=10)
    shutter_speed: str = Field(default="", max_length=20)
    iso: str = Field(default="", max_length=10)
    taken_at: Optional[datetime] = Field(default=None)
    location: str = Field(default="", max_length=100)
    tags: List[str] = Field(default=[])
    featured: bool = Field(default=False)


# 3D Project schemas
class ThreeDProjectCreate(SQLModel, table=False):
    title: str = Field(max_length=200)
    slug: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    software_used: List[str] = Field(default=[])
    render_engine: str = Field(default="", max_length=50)
    render_time: str = Field(default="", max_length=50)
    polygon_count: Optional[int] = Field(default=None)
    texture_resolution: str = Field(default="", max_length=50)
    featured_image_url: str = Field(default="", max_length=500)
    project_type: str = Field(default="", max_length=50)
    style: str = Field(default="", max_length=50)
    tags: List[str] = Field(default=[])
    featured: bool = Field(default=False)


class ThreeDRenderCreate(SQLModel, table=False):
    project_id: int
    title: str = Field(default="", max_length=200)
    description: str = Field(default="", max_length=500)
    image_url: str = Field(max_length=500)
    thumbnail_url: str = Field(default="", max_length=500)
    alt_text: str = Field(default="", max_length=200)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    render_settings: Dict[str, Any] = Field(default={})
    is_final: bool = Field(default=True)


# Site configuration schemas
class SiteConfigUpdate(SQLModel, table=False):
    site_title: Optional[str] = Field(default=None, max_length=100)
    site_description: Optional[str] = Field(default=None, max_length=500)
    owner_name: Optional[str] = Field(default=None, max_length=100)
    hero_title: Optional[str] = Field(default=None, max_length=200)
    hero_subtitle: Optional[str] = Field(default=None, max_length=300)
    hero_image_url: Optional[str] = Field(default=None, max_length=500)
    about_text: Optional[str] = Field(default=None, max_length=2000)
    about_image_url: Optional[str] = Field(default=None, max_length=500)
    contact_email: Optional[str] = Field(default=None, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=20)
    address: Optional[str] = Field(default=None, max_length=200)
    social_links: Optional[Dict[str, str]] = Field(default=None)
    theme_colors: Optional[Dict[str, str]] = Field(default=None)
    seo_keywords: Optional[List[str]] = Field(default=None)
    google_analytics_id: Optional[str] = Field(default=None, max_length=50)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
