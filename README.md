# Physical AI & Humanoid Robotics Coursebook

[![Built with Docusaurus](https://img.shields.io/badge/Built%20with-Docusaurus-green.svg)](https://docusaurus.io/)
[![AI-Driven](https://img.shields.io/badge/AI--Driven-Claude%20Code-blue.svg)](https://claude.com/product/claude-code)
[![Spec-Kit Plus](https://img.shields.io/badge/Spec--Kit-Plus-orange.svg)](https://github.com/panaversity/spec-kit-plus)

> A comprehensive academic-industrial textbook for teaching **Physical AI**, **Embodied Intelligence**, and **Humanoid Robotics** to university students, researchers, and robotics engineers.

## 📚 About

This coursebook bridges theoretical knowledge with practical application through hands-on exercises and simulations. It covers 6 core chapters ranging from foundational concepts to advanced applications in humanoid robotics.

**Target Audience**:
- Undergraduate and graduate engineering students
- Academic researchers in robotics and AI
- Professional robotics engineers

## 🚀 Quick Start

### Prerequisites

- **Node.js** 20.x LTS or higher ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/))
- **npm** or **yarn** (comes with Node.js)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/hack_book.git
cd hack_book

# Install dependencies
npm install

# Start the development server
npm start
```

The site will open at [http://localhost:3000](http://localhost:3000).

### Build

```bash
# Build for production
npm run build

# Serve the build locally
npm run serve
```

## 📖 Coursebook Structure

### Chapter 1: Foundations of Physical AI
Introduction to embodied intelligence and the intersection of AI with physical systems.

### Chapter 2: Perception Systems
Sensors, sensor fusion, environmental understanding, and object recognition.

### Chapter 3: Motion Planning & Control
Kinematics, dynamics, path planning, control systems, and manipulation.

### Chapter 4: Learning & Adaptation
Reinforcement learning, imitation learning, transfer learning, and continual learning.

### Chapter 5: System Integration
Software architecture, hardware-software integration, real-time systems, and safety.

### Chapter 6: Applications
Healthcare robotics, industrial applications, service robots, and emerging technologies.

## 🛠️ Development Workflow

This project uses **Spec-Kit Plus** for structured development:

```bash
# 1. Create a specification for a new chapter
claude /sp.specify

# 2. Generate an implementation plan
claude /sp.plan

# 3. Generate tasks breakdown
claude /sp.tasks

# 4. Implement the chapter
claude /sp.implement
```

See [quickstart.md](specs/002-ai-book-workflow/quickstart.md) for detailed instructions.

## 🧪 Testing

```bash
# Run all tests
npm run test:all

# Individual test commands
npm run test:lint        # Markdown linting
npm run test:links       # Check for broken links
npm run test:build       # Validate build
```

## 📋 Project Governance

This project follows the [Project Constitution](.specify/memory/constitution.md), which defines:

- Content standards (Markdown, style, citations)
- Chapter and section structure
- Exercise requirements
- Review and revision process
- Roles and responsibilities

## 🤖 AI-Driven Content Generation

This coursebook leverages **Claude Code** for AI-assisted content creation, ensuring:

- ✅ Consistency across chapters
- ✅ Up-to-date technical information
- ✅ Clear, pedagogical explanations
- ✅ Rigorous technical accuracy (validated by experts)

All content follows strict academic standards with proper citations and accessibility compliance (WCAG 2.1 AA).

## 📂 Project Structure

```
hack_book/
├── .specify/              # Spec-Kit Plus infrastructure
│   ├── memory/
│   │   └── constitution.md
│   ├── templates/         # SDD templates
│   └── scripts/           # Automation scripts
├── .claude/               # Claude Code commands
│   └── commands/
├── specs/                 # Feature specifications
│   └── 002-ai-book-workflow/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── research.md
│       ├── data-model.md
│       └── contracts/
├── docs/                  # Coursebook content (Markdown)
│   ├── intro.md
│   ├── chapter-01/
│   ├── chapter-02/
│   └── ...
├── static/                # Static assets
│   └── img/
├── src/                   # Custom Docusaurus components
│   ├── components/
│   ├── css/
│   └── pages/
├── docusaurus.config.js   # Docusaurus configuration
├── sidebars.js            # Sidebar navigation
└── package.json
```

## 🤝 Contributing

We welcome contributions from the community! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Ways to contribute:
- 📝 Report errors or suggest improvements
- 🧪 Add new exercises or examples
- 🌍 Improve accessibility
- 📚 Enhance documentation

## 📄 License

[LICENSE TBD] – This work is free and accessible to all learners.

## 🔗 Links

- **Live Site**: [https://YOUR_USERNAME.github.io/hack_book/](https://YOUR_USERNAME.github.io/hack_book/)
- **GitHub Repository**: [https://github.com/YOUR_USERNAME/hack_book](https://github.com/YOUR_USERNAME/hack_book)
- **Spec-Kit Plus**: [https://github.com/panaversity/spec-kit-plus](https://github.com/panaversity/spec-kit-plus)
- **Claude Code**: [https://www.claude.com/product/claude-code](https://www.claude.com/product/claude-code)

## 📧 Contact

For questions, suggestions, or feedback:
- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/hack_book/issues)
- **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/hack_book/discussions)

---

**Built with ❤️ using AI-driven development**

*Last updated: 2025-12-01*
