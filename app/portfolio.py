from nicegui import ui
import logging
from app.services import PortfolioService, SeedDataService
from app.models import ContactMessageCreate, ProjectType

logger = logging.getLogger(__name__)


def apply_glassmorphism_theme():
    """Apply glassmorphism theme and custom styles."""
    ui.add_head_html("""
    <style>
        /* Glassmorphism base styles */
        .glass-card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        }
        
        .glass-card-dark {
            background: rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);
        }
        
        .glass-button {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .glass-button:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(31, 38, 135, 0.5);
        }
        
        /* Gradient backgrounds */
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .gradient-purple {
            background: linear-gradient(135deg, #8B5CF6 0%, #A78BFA 100%);
        }
        
        .gradient-blue {
            background: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        }
        
        /* Navigation styles */
        .nav-glass {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        /* Text styles */
        .hero-title {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Project card hover effects */
        .project-card {
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .project-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 25px 50px rgba(31, 38, 135, 0.5);
        }
        
        /* Form styles */
        .glass-input {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: white;
        }
        
        .glass-input::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }
        
        /* Animation */
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }
        
        .floating {
            animation: float 6s ease-in-out infinite;
        }
        
        /* Scroll animations */
        .fade-in {
            opacity: 0;
            transform: translateY(30px);
            transition: all 0.8s ease;
        }
        
        .fade-in.visible {
            opacity: 1;
            transform: translateY(0);
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            .glass-card {
                backdrop-filter: blur(15px);
            }
        }
    </style>
    
    <script>
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        // Observe elements when DOM is ready
        document.addEventListener('DOMContentLoaded', () => {
            document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
        });
    </script>
    """)

    # Set color theme
    ui.colors(
        primary="#667eea",
        secondary="#764ba2",
        accent="#A78BFA",
        positive="#10B981",
        negative="#EF4444",
        warning="#F59E0B",
        info="#3B82F6",
    )


def create_navigation():
    """Create glassmorphism navigation bar."""
    with ui.row().classes("w-full nav-glass fixed top-0 z-50 px-6 py-4"):
        with ui.row().classes("w-full max-w-7xl mx-auto items-center justify-between"):
            # Logo
            ui.link("Alexandra Smith", "/").classes("text-white text-xl font-bold no-underline")

            # Navigation links
            with ui.row().classes("items-center gap-6 hidden md:flex"):
                ui.link("Work", "/work").classes("text-white/80 hover:text-white no-underline transition-colors")
                ui.link("Photography", "/photography").classes(
                    "text-white/80 hover:text-white no-underline transition-colors"
                )
                ui.link("3D Design", "/3d-design").classes(
                    "text-white/80 hover:text-white no-underline transition-colors"
                )
                ui.link("About", "/about").classes("text-white/80 hover:text-white no-underline transition-colors")
                ui.link("Contact", "/contact").classes("glass-button text-white px-4 py-2 rounded-lg no-underline")


def create_hero_section(config=None, owner=None):
    """Create hero section with glassmorphism design."""
    hero_title = config.hero_title if config else "Creating Digital Experiences & Capturing Moments"
    hero_subtitle = config.hero_subtitle if config else "UI/UX Designer & Photographer passionate about storytelling"

    with ui.column().classes("w-full min-h-screen gradient-bg flex items-center justify-center px-6 pt-20"):
        with ui.column().classes("max-w-4xl mx-auto text-center fade-in"):
            # Animated avatar
            if owner and owner.bio:
                ui.image(
                    "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face"
                ).classes("w-32 h-32 rounded-full mx-auto mb-8 floating shadow-2xl")

            # Main title
            ui.label(hero_title).classes("text-4xl md:text-6xl font-bold text-white mb-6 leading-tight")

            # Subtitle
            ui.label(hero_subtitle).classes("text-lg md:text-xl text-white/80 mb-12 max-w-2xl mx-auto leading-relaxed")

            # Action buttons
            with ui.row().classes("gap-4 justify-center"):
                ui.link("View My Work", "/work").classes(
                    "glass-button text-white px-8 py-4 rounded-xl font-semibold no-underline"
                )
                ui.link("Get In Touch", "/contact").classes(
                    "bg-white/20 text-white px-8 py-4 rounded-xl font-semibold no-underline hover:bg-white/30 transition-colors"
                )


def create_featured_work_section():
    """Create featured work showcase section."""
    projects = PortfolioService.get_featured_projects(limit=6)

    with ui.column().classes("w-full py-20 px-6"):
        with ui.column().classes("max-w-7xl mx-auto"):
            # Section header
            with ui.column().classes("text-center mb-16 fade-in"):
                ui.label("Featured Work").classes("text-3xl md:text-4xl font-bold text-gray-800 mb-4")
                ui.label("A selection of my recent projects and creative endeavors").classes(
                    "text-lg text-gray-600 max-w-2xl mx-auto"
                )

            # Projects grid
            if projects:
                with ui.row().classes("gap-6 justify-center flex-wrap"):
                    for project in projects:
                        create_project_card(project)
            else:
                with ui.column().classes("text-center py-12"):
                    ui.label("No featured projects yet").classes("text-gray-500 text-lg")


def create_project_card(project):
    """Create a glassmorphism project card."""
    with ui.card().classes("glass-card project-card rounded-2xl overflow-hidden w-80 fade-in"):
        # Project image
        ui.image(
            project.thumbnail_url or "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300&fit=crop"
        ).classes("w-full h-48 object-cover")

        # Project info
        with ui.column().classes("p-6"):
            ui.label(project.title).classes("text-xl font-bold text-white mb-2")
            ui.label(project.description).classes("text-white/80 text-sm mb-4")

            # Tags
            if project.tags:
                with ui.row().classes("gap-2 mb-4 flex-wrap"):
                    for tag in project.tags[:3]:  # Show max 3 tags
                        ui.label(tag).classes("bg-white/20 text-white text-xs px-3 py-1 rounded-full")

            # View project button
            def view_project(project_slug=project.slug):
                if project_slug:
                    ui.navigate.to(f"/project/{project_slug}")

            ui.button("View Project", on_click=view_project).classes(
                "glass-button w-full text-white py-2 rounded-lg font-medium"
            )


def create_services_section():
    """Create services overview section."""
    services = [
        {
            "title": "UI/UX Design",
            "description": "Creating intuitive and beautiful digital experiences that users love",
            "icon": "🎨",
            "gradient": "gradient-purple",
        },
        {
            "title": "Photography",
            "description": "Capturing moments and emotions through creative visual storytelling",
            "icon": "📸",
            "gradient": "gradient-blue",
        },
        {
            "title": "3D Design",
            "description": "Bringing ideas to life with stunning 3D visualizations and renders",
            "icon": "🎭",
            "gradient": "gradient-purple",
        },
    ]

    with ui.column().classes("w-full py-20 px-6 bg-gray-50"):
        with ui.column().classes("max-w-7xl mx-auto"):
            # Section header
            with ui.column().classes("text-center mb-16 fade-in"):
                ui.label("What I Do").classes("text-3xl md:text-4xl font-bold text-gray-800 mb-4")
                ui.label("Bringing creativity to life through multiple disciplines").classes(
                    "text-lg text-gray-600 max-w-2xl mx-auto"
                )

            # Services grid
            with ui.row().classes("gap-8 justify-center flex-wrap"):
                for service in services:
                    with ui.card().classes(
                        f"glass-card rounded-2xl p-8 w-80 text-center fade-in {service['gradient']}"
                    ):
                        ui.label(service["icon"]).classes("text-6xl mb-4")
                        ui.label(service["title"]).classes("text-2xl font-bold text-white mb-4")
                        ui.label(service["description"]).classes("text-white/80 leading-relaxed")


def create_contact_form():
    """Create glassmorphism contact form."""
    name_input = ui.input("Name").classes("glass-input w-full mb-4 text-white").props("filled dark")
    email_input = ui.input("Email").classes("glass-input w-full mb-4 text-white").props("filled dark")
    subject_input = ui.input("Subject").classes("glass-input w-full mb-4 text-white").props("filled dark")
    message_input = ui.textarea("Message").classes("glass-input w-full mb-6 text-white").props("filled dark rows=5")

    async def send_message():
        # Validate inputs
        if not all([name_input.value, email_input.value, subject_input.value, message_input.value]):
            ui.notify("Please fill in all fields", type="negative")
            return

        try:
            # Create message
            message_data = ContactMessageCreate(
                name=name_input.value, email=email_input.value, subject=subject_input.value, message=message_input.value
            )

            PortfolioService.create_contact_message(message_data)

            # Success feedback
            ui.notify("Message sent successfully! I'll get back to you soon.", type="positive")

            # Clear form
            name_input.value = ""
            email_input.value = ""
            subject_input.value = ""
            message_input.value = ""

        except Exception as e:
            logger.error(f"Error sending contact message: {str(e)}")
            ui.notify(f"Error sending message: {str(e)}", type="negative")

    ui.button("Send Message", on_click=send_message).classes(
        "glass-button w-full text-white py-3 rounded-lg font-semibold text-lg"
    )


def create_footer():
    """Create glassmorphism footer."""
    config = PortfolioService.get_site_config()

    with ui.column().classes("w-full bg-gray-900 py-12 px-6 mt-20"):
        with ui.column().classes("max-w-7xl mx-auto text-center"):
            # Name and title
            ui.label("Alexandra Smith").classes("text-2xl font-bold text-white mb-2")
            ui.label("UI/UX Designer & Photographer").classes("text-gray-400 mb-6")

            # Social links
            if config and config.social_links:
                with ui.row().classes("gap-6 justify-center mb-8"):
                    for platform, url in config.social_links.items():
                        ui.link(platform.capitalize(), url, new_tab=True).classes(
                            "text-gray-400 hover:text-white transition-colors no-underline"
                        )

            # Copyright
            ui.label("© 2024 Alexandra Smith. All rights reserved.").classes("text-gray-500 text-sm")


def create():
    """Create the portfolio website."""
    # Initialize theme
    apply_glassmorphism_theme()

    # Seed sample data if needed
    SeedDataService.create_sample_data()

    @ui.page("/")
    def homepage():
        config = PortfolioService.get_site_config()
        owner = PortfolioService.get_portfolio_owner()

        create_navigation()
        create_hero_section(config, owner)
        create_featured_work_section()
        create_services_section()
        create_footer()

    @ui.page("/work")
    def work_page():
        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-7xl mx-auto py-12"):
                # Page header
                with ui.column().classes("text-center mb-12 fade-in"):
                    ui.label("My Work").classes("text-4xl md:text-5xl font-bold text-white mb-4")
                    ui.label("UI/UX Design Projects & Case Studies").classes("text-xl text-white/80")

                # Projects grid
                projects = PortfolioService.get_projects_by_type(ProjectType.UI_UX)
                if projects:
                    with ui.row().classes("gap-6 justify-center flex-wrap"):
                        for project in projects:
                            create_project_card(project)
                else:
                    ui.label("No projects available yet").classes("text-white/60 text-center text-lg")

        create_footer()

    @ui.page("/photography")
    def photography_page():
        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-7xl mx-auto py-12"):
                # Page header
                with ui.column().classes("text-center mb-12 fade-in"):
                    ui.label("Photography").classes("text-4xl md:text-5xl font-bold text-white mb-4")
                    ui.label("Capturing life through the lens").classes("text-xl text-white/80")

                # Galleries grid
                galleries = PortfolioService.get_featured_galleries()
                if galleries:
                    with ui.row().classes("gap-6 justify-center flex-wrap"):
                        for gallery in galleries:
                            create_gallery_card(gallery)
                else:
                    ui.label("No galleries available yet").classes("text-white/60 text-center text-lg")

        create_footer()

    @ui.page("/3d-design")
    def three_d_page():
        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-7xl mx-auto py-12"):
                # Page header
                with ui.column().classes("text-center mb-12 fade-in"):
                    ui.label("3D Design").classes("text-4xl md:text-5xl font-bold text-white mb-4")
                    ui.label("Static renders and 3D visualizations").classes("text-xl text-white/80")

                # 3D projects grid
                projects = PortfolioService.get_featured_3d_projects()
                if projects:
                    with ui.row().classes("gap-6 justify-center flex-wrap"):
                        for project in projects:
                            create_3d_project_card(project)
                else:
                    ui.label("No 3D projects available yet").classes("text-white/60 text-center text-lg")

        create_footer()

    @ui.page("/about")
    def about_page():
        config = PortfolioService.get_site_config()
        owner = PortfolioService.get_portfolio_owner()

        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-4xl mx-auto py-12"):
                # About content
                with ui.row().classes("gap-12 items-center flex-wrap fade-in"):
                    # Image
                    ui.image(
                        config.about_image_url
                        if config
                        else "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop"
                    ).classes("w-80 h-80 rounded-2xl object-cover shadow-2xl")

                    # Text content
                    with ui.column().classes("flex-1 min-w-80"):
                        ui.label("About Me").classes("text-4xl font-bold text-white mb-6")

                        about_text = (
                            owner.bio
                            if owner
                            else "I'm a passionate designer and photographer with a love for creating beautiful, functional experiences."
                        )
                        ui.label(about_text).classes("text-lg text-white/80 leading-relaxed mb-6")

                        if owner:
                            ui.label(f"Location: {owner.location}").classes("text-white/70 mb-2")
                            ui.label(f"Email: {owner.email}").classes("text-white/70 mb-6")

                        ui.link("Get In Touch", "/contact").classes(
                            "glass-button text-white px-6 py-3 rounded-lg no-underline font-medium"
                        )

        create_footer()

    @ui.page("/contact")
    def contact_page():
        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-2xl mx-auto py-12"):
                # Contact header
                with ui.column().classes("text-center mb-12 fade-in"):
                    ui.label("Get In Touch").classes("text-4xl md:text-5xl font-bold text-white mb-4")
                    ui.label("Let's discuss your next project").classes("text-xl text-white/80")

                # Contact form
                with ui.card().classes("glass-card rounded-2xl p-8 fade-in"):
                    create_contact_form()

        create_footer()

    @ui.page("/project/{slug}")
    def project_detail_page(slug: str):
        project = PortfolioService.get_project_by_slug(slug)
        if not project:
            ui.navigate.to("/work")
            return

        create_navigation()

        with ui.column().classes("w-full min-h-screen gradient-bg pt-20 px-6"):
            with ui.column().classes("max-w-4xl mx-auto py-12"):
                # Project header
                with ui.column().classes("text-center mb-12 fade-in"):
                    ui.label(project.title).classes("text-4xl md:text-5xl font-bold text-white mb-4")
                    ui.label(project.description).classes("text-xl text-white/80 mb-6")

                    # Project image
                    if project.cover_image_url:
                        ui.image(project.cover_image_url).classes("w-full max-w-3xl mx-auto rounded-2xl shadow-2xl")

                # Project details
                with ui.card().classes("glass-card rounded-2xl p-8 fade-in mt-12"):
                    if project.detailed_description:
                        ui.label("Project Overview").classes("text-2xl font-bold text-white mb-4")
                        ui.label(project.detailed_description).classes("text-white/80 leading-relaxed mb-6")

                    # Project info
                    with ui.row().classes("gap-8 flex-wrap"):
                        if project.client_name:
                            with ui.column():
                                ui.label("Client").classes("text-white font-semibold mb-1")
                                ui.label(project.client_name).classes("text-white/80")

                        if project.project_duration:
                            with ui.column():
                                ui.label("Duration").classes("text-white font-semibold mb-1")
                                ui.label(project.project_duration).classes("text-white/80")

                    # Technologies
                    if project.technologies:
                        ui.label("Technologies").classes("text-white font-semibold mb-2 mt-6")
                        with ui.row().classes("gap-2 flex-wrap"):
                            for tech in project.technologies:
                                ui.label(tech).classes("bg-white/20 text-white text-sm px-3 py-1 rounded-full")

        create_footer()


def create_gallery_card(gallery):
    """Create a gallery card for photography section."""
    with ui.card().classes("glass-card project-card rounded-2xl overflow-hidden w-80 fade-in"):
        # Gallery cover image
        ui.image(
            gallery.cover_image_url
            or "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400&h=300&fit=crop"
        ).classes("w-full h-48 object-cover")

        # Gallery info
        with ui.column().classes("p-6"):
            ui.label(gallery.title).classes("text-xl font-bold text-white mb-2")
            ui.label(gallery.description).classes("text-white/80 text-sm mb-4")

            if gallery.location:
                ui.label(f"📍 {gallery.location}").classes("text-white/70 text-sm mb-4")

            # View gallery button
            def view_gallery(gallery_slug=gallery.slug):
                if gallery_slug:
                    ui.navigate.to(f"/gallery/{gallery_slug}")

            ui.button("View Gallery", on_click=view_gallery).classes(
                "glass-button w-full text-white py-2 rounded-lg font-medium"
            )


def create_3d_project_card(project):
    """Create a 3D project card."""
    with ui.card().classes("glass-card project-card rounded-2xl overflow-hidden w-80 fade-in"):
        # Project image
        ui.image(
            project.featured_image_url
            or "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=400&h=300&fit=crop"
        ).classes("w-full h-48 object-cover")

        # Project info
        with ui.column().classes("p-6"):
            ui.label(project.title).classes("text-xl font-bold text-white mb-2")
            ui.label(project.description).classes("text-white/80 text-sm mb-4")

            # Software used
            if project.software_used:
                with ui.row().classes("gap-2 mb-4 flex-wrap"):
                    for software in project.software_used[:2]:  # Show max 2
                        ui.label(software).classes("bg-white/20 text-white text-xs px-3 py-1 rounded-full")

            # View project button
            def view_renders(project_slug=project.slug):
                if project_slug:
                    ui.navigate.to(f"/3d-project/{project_slug}")

            ui.button("View Renders", on_click=view_renders).classes(
                "glass-button w-full text-white py-2 rounded-lg font-medium"
            )
