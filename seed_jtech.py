"""
Seed script: pre-loads all 11 JTech courses + 6 recommended learning pathways
with module structure + sample lessons.

Run:  python manage.py shell < scripts/seed_jtech.py
Or:   python manage.py load_jtech_data   (after registering the command)
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jtech_lms.settings')
django.setup()

from decimal import Decimal
from courses.models import Programme, Course, Module, Lesson, LearningPathway, PathwayStep
from accounts.models import User

# ---------- COURSE DATA ----------
# Each entry: (name, duration_months, monthly_fee, icon, color, description, modules)
# Each module: (title, lessons) where each lesson: (title, type, duration_min, is_preview, description)

COURSES = [
    {
        "name": "Spoken English",
        "duration_months": 3,
        "monthly_fee": Decimal("499"),
        "icon": "comments",
        "color": "#0ea5e9",
        "description": "Build fluency and confidence in everyday spoken English — from introductions to interviews.",
        "modules": [
            ("Foundations of Spoken English", [
                ("Sounds & Pronunciation", "video", 25, True, "Phonetics basics — vowels, consonants, common Indian-English pitfalls."),
                ("Common Words & Greetings", "video", 20, False, "Daily-use vocabulary, formal and informal greetings."),
                ("Building Simple Sentences", "video", 30, False, "Subject-verb-object structure, question forms."),
            ]),
            ("Conversation Practice", [
                ("Self Introduction", "video", 25, False, "Structured way to introduce yourself in any setting."),
                ("Asking Questions & Clarifying", "video", 30, False, "Wh-questions, polite clarification phrases."),
                ("Roleplay: At the Shop", "live", 45, False, "Live roleplay session — buying groceries, asking for help."),
                ("Group Discussion Basics", "video", 35, False, "How to enter a conversation, agree, disagree politely."),
            ]),
            ("Real-World English", [
                ("Telephone & Video Calls", "video", 30, False, "Professional phone etiquette, video call phrases."),
                ("Job Interview English", "video", 40, False, "Common interview questions and confident answers."),
                ("Public Speaking Basics", "video", 35, False, "Overcoming stage fear, structuring a 3-minute talk."),
                ("Final Assessment & Feedback", "assignment", 60, False, "Recorded self-introduction + interview Q&A submission."),
            ]),
        ],
    },
    {
        "name": "Basic Computer",
        "duration_months": 3,
        "monthly_fee": Decimal("499"),
        "icon": "desktop",
        "color": "#16a34a",
        "description": "Master computer fundamentals — hardware, OS, internet, MS Office basics.",
        "modules": [
            ("Computer Fundamentals", [
                ("What is a Computer?", "video", 20, True, "Hardware vs software, input/output devices."),
                ("Operating System Basics", "video", 25, False, "Windows desktop, files, folders, settings."),
                ("File Management", "video", 30, False, "Creating, moving, organising files and folders."),
            ]),
            ("Typing & Internet", [
                ("Typing Practice", "video", 30, False, "Touch typing basics, speed building exercises."),
                ("Internet & Browsing", "video", 25, False, "Browsers, search engines, safe browsing."),
                ("Email Basics", "video", 30, False, "Gmail account, composing, replying, attachments."),
                ("Online Safety", "video", 25, False, "Passwords, phishing, scams to avoid."),
            ]),
            ("MS Office Introduction", [
                ("MS Word Basics", "video", 35, False, "Typing documents, formatting, saving."),
                ("MS Excel Basics", "video", 35, False, "Cells, simple formulas, sorting."),
                ("MS PowerPoint Basics", "video", 30, False, "Slides, text, simple animation."),
                ("Final Project: Create a Resume", "assignment", 60, False, "Build a one-page resume in Word."),
            ]),
        ],
    },
    {
        "name": "Advanced Excel",
        "duration_months": 2,
        "monthly_fee": Decimal("699"),
        "icon": "file-excel",
        "color": "#15803d",
        "description": "Power-user Excel — advanced formulas, pivot tables, dashboards, automation.",
        "modules": [
            ("Advanced Formulas", [
                ("Lookup Functions (VLOOKUP, XLOOKUP, INDEX-MATCH)", "video", 40, True, "Master lookups with real examples."),
                ("Logical & Text Functions", "video", 35, False, "IF, IFS, AND, OR, LEFT, RIGHT, MID, CONCAT."),
                ("Date & Time Functions", "video", 30, False, "DATE, EOMONTH, NETWORKDAYS, EDATE."),
                ("Array Formulas", "video", 40, False, "Dynamic arrays, FILTER, SORT, UNIQUE."),
            ]),
            ("Data Analysis", [
                ("Pivot Tables Deep Dive", "video", 45, False, "Building, grouping, calculated fields."),
                ("Pivot Charts & Slicers", "video", 35, False, "Interactive dashboards."),
                ("Power Query Basics", "video", 40, False, "Importing and cleaning data from multiple sources."),
                ("What-If Analysis", "video", 30, False, "Goal Seek, Scenario Manager, Data Tables."),
            ]),
            ("Dashboards & Automation", [
                ("Building a Sales Dashboard", "assignment", 90, False, "End-to-end dashboard project."),
                ("Macros & VBA Basics", "video", 45, False, "Recording macros, simple VBA editing."),
                ("Final Assessment", "quiz", 45, False, "Comprehensive Excel skill test."),
            ]),
        ],
    },
    {
        "name": "Tally Prime + GST",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "calculator",
        "color": "#0891b2",
        "description": "Complete Tally Prime with GST — accounting, inventory, taxation, returns.",
        "modules": [
            ("Tally Prime Basics", [
                ("Installation & Company Creation", "video", 25, True, "Install Tally Prime, set up company."),
                ("Chart of Accounts", "video", 30, False, "Ledgers, groups, accounting principles."),
                ("Voucher Entry", "video", 40, False, "Payment, receipt, contra, journal vouchers."),
            ]),
            ("Inventory Management", [
                ("Stock Groups & Items", "video", 35, False, "Creating inventory masters."),
                ("Godowns & Batches", "video", 30, False, "Multi-location stock tracking."),
                ("Purchase & Sales Vouchers", "video", 40, False, "Complete inventory voucher flow."),
            ]),
            ("GST in Tally", [
                ("GST Setup", "video", 35, False, "Configuring GST in Tally Prime."),
                ("GST Sales & Purchase", "video", 45, False, "Tax-wise invoicing."),
                ("GSTR-1 Generation", "video", 40, False, "Preparing and exporting GSTR-1."),
                ("GSTR-3B Generation", "video", 35, False, "Monthly return preparation."),
            ]),
            ("Reports & Final Project", [
                ("Balance Sheet & P&L", "video", 30, False, "Final accounts in Tally."),
                ("Real-World Project: Trading Company", "assignment", 120, False, "Complete 1-month books for a sample business."),
            ]),
        ],
    },
    {
        "name": "Practical Accounting",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "balance-scale",
        "color": "#7c3aed",
        "description": "Hands-on accounting — from journal entries to final accounts, with real business cases.",
        "modules": [
            ("Accounting Fundamentals", [
                ("Double-Entry System", "video", 30, True, "Debits, credits, the accounting equation."),
                ("Journal & Ledger", "video", 35, False, "Recording transactions, posting to ledgers."),
                ("Trial Balance", "video", 25, False, "Detecting and fixing errors."),
            ]),
            ("Indian Accounting Standards", [
                ("Ind AS Overview", "video", 30, False, "Key standards every accountant should know."),
                ("Depreciation as per Companies Act", "video", 35, False, "Rates, methods, schedules."),
                ("Bank Reconciliation", "video", 35, False, "BRS step by step with example."),
            ]),
            ("Final Accounts", [
                ("Trading & P&L Account", "video", 40, False, "Preparing P&L for trading and service businesses."),
                ("Balance Sheet", "video", 35, False, "Classification, marshalling."),
                ("Cash Flow Statement", "video", 40, False, "Indirect method step-by-step."),
            ]),
            ("Practical Cases", [
                ("Case 1: Retail Shop", "assignment", 90, False, "Full accounting cycle for a small retailer."),
                ("Case 2: Service Company", "assignment", 90, False, "Service business with GST."),
            ]),
        ],
    },
    {
        "name": "FinTech",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "money-bill-wave",
        "color": "#059669",
        "description": "Digital payments, UPI, blockchain, regtech, and the future of Indian finance.",
        "modules": [
            ("Digital Payments Landscape", [
                ("Evolution of Payments in India", "video", 25, True, "From cash to UPI — the journey."),
                ("UPI Architecture Deep Dive", "video", 40, False, "How UPI works behind the scenes."),
                ("Wallets, BBPS, AePS", "video", 30, False, "Other payment rails."),
            ]),
            ("Banking Tech", [
                ("Core Banking Systems", "video", 30, False, "How banks process transactions."),
                ("Lending Tech & BNPL", "video", 35, False, "Digital lending, credit scoring."),
                ("Open Banking & APIs", "video", 30, False, "Account aggregator framework."),
            ]),
            ("Crypto & Blockchain", [
                ("Blockchain Fundamentals", "video", 40, False, "Distributed ledger, consensus."),
                ("Cryptocurrencies & Tokens", "video", 35, False, "Bitcoin, Ethereum, stablecoins."),
                ("India's CBDC: e-Rupee", "video", 25, False, "RBI's digital currency."),
            ]),
            ("RegTech & Future", [
                ("KYC, AML & RegTech", "video", 30, False, "Compliance automation."),
                ("InsurTech Overview", "video", 30, False, "Tech in insurance."),
                ("Capstone: FinTech Startup Pitch", "assignment", 120, False, "Pitch a FinTech product for tier-2/3 India."),
            ]),
        ],
    },
    {
        "name": "Python Programming",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "python",
        "color": "#3776ab",
        "description": "Learn Python from zero to building real apps — variables, OOP, files, web scraping.",
        "modules": [
            ("Python Basics", [
                ("Installing Python & IDE", "video", 15, True, "Setup Python + VS Code."),
                ("Variables & Data Types", "video", 30, False, "int, float, str, bool, type conversion."),
                ("Operators & Input", "video", 25, False, "Arithmetic, comparison, input()."),
                ("Strings In-Depth", "video", 35, False, "Slicing, methods, f-strings."),
            ]),
            ("Control Flow", [
                ("If-Else & Match", "video", 30, False, "Conditional logic, Python 3.10 match."),
                ("Loops (for & while)", "video", 35, False, "Iteration, break, continue."),
                ("Functions", "video", 40, False, "Defining, parameters, return, scope."),
                ("Mini Project: Calculator", "assignment", 60, False, "Build a CLI calculator."),
            ]),
            ("Data Structures", [
                ("Lists & Tuples", "video", 40, False, "Mutable vs immutable, methods."),
                ("Dictionaries & Sets", "video", 40, False, "Key-value, sets, lookup performance."),
                ("Comprehensions", "video", 25, False, "List/dict/set comprehensions."),
            ]),
            ("OOP & Beyond", [
                ("Classes & Objects", "video", 45, False, "Object-oriented programming."),
                ("Inheritance & Polymorphism", "video", 40, False, "Reusing code, overriding."),
                ("File Handling", "video", 30, False, "Read/write text, CSV, JSON."),
                ("Web Scraping Basics", "video", 40, False, "Requests + BeautifulSoup."),
                ("Final Project: Weather App", "assignment", 120, False, "Build a CLI weather app using an API."),
            ]),
        ],
    },
    {
        "name": "Django Web Development",
        "duration_months": 4,
        "monthly_fee": Decimal("1499"),
        "icon": "code",
        "color": "#0d6efd",
        "description": "Build production web apps with Django — models, views, templates, auth, deployment.",
        "modules": [
            ("Django Foundations", [
                ("Why Django? Project vs App", "video", 25, True, "Django philosophy, project structure."),
                ("Your First Django App", "video", 40, False, "Setup, runserver, hello world view."),
                ("URLs & Views", "video", 35, False, "URL routing, function-based views."),
                ("Templates & Template Inheritance", "video", 40, False, "DTL, extends, blocks."),
            ]),
            ("Working with Data", [
                ("Models & Migrations", "video", 45, False, "Defining models, makemigrations, migrate."),
                ("Django ORM Queries", "video", 45, False, "CRUD, filters, related objects."),
                ("Admin Site Customisation", "video", 35, False, "Customising the admin."),
                ("Forms & ModelForms", "video", 40, False, "Handling user input safely."),
            ]),
            ("Authentication & UX", [
                ("User Authentication", "video", 45, False, "Login, logout, signup, password reset."),
                ("Class-Based Views", "video", 40, False, "ListView, DetailView, CreateView."),
                ("Middleware & Sessions", "video", 35, False, "Request/response lifecycle."),
                ("AJAX with Django", "video", 40, False, "Fetch API, CSRF, dynamic UI."),
            ]),
            ("Production-Grade", [
                ("Static Files & Media", "video", 30, False, "Static handling, user uploads."),
                ("Deployment: Linux + Gunicorn + Nginx", "video", 50, False, "Production deployment."),
                ("Email, Caching & Celery", "video", 45, False, "Async tasks, caching, email backend."),
                ("Capstone: Build a Blog/CMS", "assignment", 180, False, "Full-featured blog with auth, comments, admin."),
            ]),
        ],
    },
    {
        "name": "AI & Machine Learning",
        "duration_months": 4,
        "monthly_fee": Decimal("1499"),
        "icon": "brain",
        "color": "#dc2626",
        "description": "From ML fundamentals to neural networks — scikit-learn, TensorFlow, real projects.",
        "modules": [
            ("Math & ML Foundations", [
                ("Linear Algebra Refresher", "video", 40, True, "Vectors, matrices, dot products."),
                ("Probability & Statistics", "video", 45, False, "Distributions, mean, variance, Bayes."),
                ("What is Machine Learning?", "video", 30, False, "Supervised, unsupervised, RL."),
                ("Pandas & NumPy", "video", 50, False, "Data manipulation essentials."),
            ]),
            ("Supervised Learning", [
                ("Linear & Logistic Regression", "video", 45, False, "From scratch + scikit-learn."),
                ("Decision Trees & Random Forest", "video", 40, False, "Tree-based models."),
                ("SVM & KNN", "video", 40, False, "Distance-based classifiers."),
                ("Model Evaluation", "video", 35, False, "Accuracy, precision, recall, F1, ROC."),
            ]),
            ("Unsupervised & Deep Learning", [
                ("K-Means & PCA", "video", 40, False, "Clustering and dimensionality reduction."),
                ("Neural Networks Basics", "video", 50, False, "Perceptron, backpropagation."),
                ("Intro to TensorFlow/Keras", "video", 50, False, "Build your first NN."),
                ("CNN for Image Classification", "video", 60, False, "MNIST digit classifier."),
            ]),
            ("Real-World ML", [
                ("NLP with spaCy", "video", 45, False, "Text processing basics."),
                ("MLOps: Deploy with FastAPI", "video", 50, False, "Serving ML models."),
                ("Capstone: End-to-End ML Project", "assignment", 240, False, "Pick a dataset, train, evaluate, deploy."),
            ]),
        ],
    },
    {
        "name": "NASA Space Apps Preparation 2027",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "rocket",
        "color": "#1d4ed8",
        "description": "Prepare for NASA Space Apps Challenge 2027 — team formation, project, presentation.",
        "modules": [
            ("Understanding Space Apps", [
                ("What is NASA Space Apps Challenge?", "video", 25, True, "History, categories, success stories."),
                ("2025/26 Challenge Categories", "video", 30, False, "Themes & sample problem statements."),
                ("Past Winning Projects Analysis", "video", 40, False, "What makes a winning submission."),
            ]),
            ("Tech Skills for Space Apps", [
                ("Earth Observation Data Basics", "video", 40, False, "NASA APIs, satellite imagery."),
                ("Open Data Sources", "video", 35, False, "Where to find datasets."),
                ("Visualisation with Python", "video", 45, False, "Matplotlib, Folium maps."),
                ("Building a Quick MVP", "video", 50, False, "From idea to working demo in 48 hours."),
            ]),
            ("Team & Presentation", [
                ("Team Roles & Collaboration", "video", 30, False, "How to structure your hackathon team."),
                ("Pitching Your Project", "video", 35, False, "5-minute pitch framework."),
                ("Demo Video Best Practices", "video", 30, False, "Recording, editing, submission."),
                ("Mock Hackathon", "live", 180, False, "Simulated 48-hour challenge (over a weekend)."),
            ]),
        ],
    },
    {
        "name": "Smart India Hackathon Preparation 2027",
        "duration_months": 3,
        "monthly_fee": Decimal("999"),
        "icon": "trophy",
        "color": "#b45309",
        "description": "Prepare for SIH 2027 — problem statement selection, innovation, build, pitch.",
        "modules": [
            ("SIH Overview", [
                ("What is Smart India Hackathon?", "video", 25, True, "Structure, categories, rules."),
                ("Problem Statement Categories", "video", 30, False, "Government, industry, student innovations."),
                ("Past SIH Winners Analysis", "video", 35, False, "Case studies of winning solutions."),
            ]),
            ("Innovation & Build", [
                ("Ideation Framework", "video", 30, False, "From problem to solution design."),
                ("Tech Stack Selection", "video", 35, False, "Choosing the right tools for the problem."),
                ("Rapid Prototyping", "video", 45, False, "Building a working prototype in 36 hours."),
                ("Integration with Government APIs", "video", 40, False, "Data.gov.in, UPI, Aadhaar (where allowed)."),
            ]),
            ("Winning the Pitch", [
                ("Demo Preparation", "video", 30, False, "What judges look for."),
                ("Q&A Handling", "video", 25, False, "Anticipating judge questions."),
                ("Documentation & Submission", "video", 30, False, "PPT, code repo, video."),
                ("Mock SIH Round", "live", 180, False, "Simulated 36-hour SIH round."),
            ]),
        ],
    },
]

# ---------- LEARNING PATHWAYS ----------
PATHWAYS = [
    {
        "name": "Office & Computer Professional",
        "icon": "briefcase", "color": "#0ea5e9",
        "description": "Become office-ready with strong computer and Excel skills.",
        "steps": ["Basic Computer", "Advanced Excel"],
    },
    {
        "name": "Accounting Professional",
        "icon": "ledger", "color": "#0891b2",
        "description": "Complete accounting career path — from computer basics to Tally + practical accounting.",
        "steps": ["Basic Computer", "Advanced Excel", "Tally Prime + GST", "Practical Accounting"],
    },
    {
        "name": "FinTech Professional",
        "icon": "chart-line", "color": "#059669",
        "description": "Specialise in financial technology with accounting + FinTech knowledge.",
        "steps": ["Advanced Excel", "Practical Accounting", "FinTech"],
    },
    {
        "name": "Python Full Stack Developer",
        "icon": "layer-group", "color": "#3776ab",
        "description": "Go from Python basics to building production web apps with Django.",
        "steps": ["Python Programming", "Django Web Development"],
    },
    {
        "name": "AI Developer",
        "icon": "robot", "color": "#dc2626",
        "description": "Become an AI engineer — Python foundations to ML/AI project deployment.",
        "steps": ["Python Programming", "AI & Machine Learning"],
    },
    {
        "name": "Innovation & Research",
        "icon": "lightbulb", "color": "#b45309",
        "description": "Prepare for top hackathons with Python + data science + competition prep.",
        "steps": ["Python Programming", "AI & Machine Learning",
                  "NASA Space Apps Preparation 2027"],
    },
]


def seed():
    print("Seeding JTech LMS data...")

    # Create default admin if missing
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            'admin', 'admin@jtechlearning.in', 'admin123', role=User.Role.ADMIN
        )
        print("  ✓ Created superuser: admin / admin123")

    # Create a demo instructor
    instructor, _ = User.objects.get_or_create(
        username='instructor_demo',
        defaults={
            'email': 'instructor@jtechlearning.in',
            'first_name': 'Demo',
            'last_name': 'Instructor',
            'role': User.Role.INSTRUCTOR,
            'specialization': 'Python, Django, AI/ML',
            'experience_years': 5,
        }
    )
    if not instructor.password.startswith('pbkdf2'):
        instructor.set_password('instructor123')
        instructor.save()
    print(f"  ✓ Demo instructor: instructor_demo / instructor123")

    # Programmes + Courses
    for cdata in COURSES:
        programme, created = Programme.objects.get_or_create(
            name=cdata['name'],
            defaults={
                'duration_months': cdata['duration_months'],
                'monthly_fee': cdata['monthly_fee'],
                'icon': cdata['icon'],
                'color': cdata['color'],
                'description': cdata['description'],
                'order': COURSES.index(cdata),
            }
        )
        if created:
            print(f"  ✓ Programme: {programme.name}  (₹{programme.monthly_fee}/mo × "
                  f"{programme.duration_months}m = ₹{programme.total_fee})")

        # One course per programme (self-paced)
        course, created = Course.objects.get_or_create(
            programme=programme,
            defaults={
                'title': programme.name,
                'subtitle': cdata['description'][:120],
                'description': cdata['description'],
                'target_audience': 'Students and professionals seeking structured learning',
                'is_self_paced': True,
            }
        )
        if created:
            course.instructors.add(instructor)
            print(f"    └─ Course: {course.title}")

        for m_order, (m_title, lessons) in enumerate(cdata['modules']):
            module, _ = Module.objects.get_or_create(
                course=course, order=m_order,
                defaults={'title': m_title}
            )
            for l_order, (l_title, l_type, l_dur, l_preview, l_desc) in enumerate(lessons):
                Lesson.objects.update_or_create(
                    module=module, order=l_order,
                    defaults={
                        'title': l_title,
                        'lesson_type': l_type,
                        'duration_minutes': l_dur,
                        'is_preview': l_preview,
                        'description': l_desc,
                        'content': '' if l_type != 'reading' else l_desc,
                    }
                )

    # Pathways
    for pdata in PATHWAYS:
        pathway, created = LearningPathway.objects.get_or_create(
            name=pdata['name'],
            defaults={
                'description': pdata['description'],
                'icon': pdata['icon'],
                'badge_color': pdata['color'],
                'order': PATHWAYS.index(pdata),
            }
        )
        if created:
            print(f"  ✓ Pathway: {pathway.name}")
        for s_order, prog_name in enumerate(pdata['steps']):
            try:
                prog = Programme.objects.get(name=prog_name)
                PathwayStep.objects.update_or_create(
                    pathway=pathway, order=s_order,
                    defaults={'programme': prog}
                )
            except Programme.DoesNotExist:
                print(f"  ! WARNING: programme '{prog_name}' not found for pathway '{pathway.name}'")

    print("\n✅ Seeding complete.")
    print(f"   Programmes: {Programme.objects.count()}")
    print(f"   Courses:    {Course.objects.count()}")
    print(f"   Modules:    {Module.objects.count()}")
    print(f"   Lessons:    {Lesson.objects.count()}")
    print(f"   Pathways:   {LearningPathway.objects.count()}")
    print(f"   Pathway Steps: {PathwayStep.objects.count()}")
    print("\nLogin: admin / admin123  (admin)")
    print("Login: instructor_demo / instructor123  (instructor)")


if __name__ == '__main__':
    seed()
