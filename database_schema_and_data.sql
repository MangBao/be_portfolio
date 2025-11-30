-- ============================================
-- Database Schema and Data Export
-- Generated from backup: db_cluster-22-06-2025@05-20-09.backup
-- ============================================

-- Drop existing tables if they exist (in reverse order of dependencies)
DROP TABLE IF EXISTS public."user" CASCADE;
DROP TABLE IF EXISTS public.skill CASCADE;
DROP TABLE IF EXISTS public.project CASCADE;
DROP TABLE IF EXISTS public.menu CASCADE;
DROP TABLE IF EXISTS public.experience CASCADE;
DROP TABLE IF EXISTS public.contact CASCADE;
DROP TABLE IF EXISTS public.alembic_version CASCADE;
DROP TABLE IF EXISTS public.about CASCADE;

-- Drop sequences if they exist
DROP SEQUENCE IF EXISTS public.user_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.skill_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.project_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.menu_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.experience_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.contact_id_seq CASCADE;
DROP SEQUENCE IF EXISTS public.about_id_seq CASCADE;

-- ============================================
-- CREATE SEQUENCES
-- ============================================

CREATE SEQUENCE public.about_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.contact_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.experience_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.menu_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.project_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.skill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE SEQUENCE public.user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- ============================================
-- CREATE TABLES
-- ============================================

CREATE TABLE public.about (
    id integer NOT NULL DEFAULT nextval('public.about_id_seq'::regclass),
    title character varying(200) NOT NULL,
    content text NOT NULL,
    image character varying(200),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);

CREATE TABLE public.contact (
    id integer NOT NULL DEFAULT nextval('public.contact_id_seq'::regclass),
    name character varying(100) NOT NULL,
    email character varying(120) NOT NULL,
    subject character varying(200) NOT NULL,
    content text NOT NULL,
    status character varying(20),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public.experience (
    id integer NOT NULL DEFAULT nextval('public.experience_id_seq'::regclass),
    company_name character varying(200) NOT NULL,
    role_name character varying(200) NOT NULL,
    desc_role text,
    company_location character varying(200),
    start_date character varying(10) NOT NULL,
    end_date character varying(10),
    is_current boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public.menu (
    id integer NOT NULL DEFAULT nextval('public.menu_id_seq'::regclass),
    title character varying(200),
    menu_name character varying(50) NOT NULL,
    menu_url character varying(100) NOT NULL,
    menu_order integer,
    is_active boolean,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public.project (
    id integer NOT NULL DEFAULT nextval('public.project_id_seq'::regclass),
    title character varying(200) NOT NULL,
    image character varying(200),
    description text NOT NULL,
    role text NOT NULL,
    project_url character varying(200),
    github_url character varying(200),
    technologies character varying(200),
    start_date character varying(10) NOT NULL,
    end_date character varying(10),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public.skill (
    id integer NOT NULL DEFAULT nextval('public.skill_id_seq'::regclass),
    skill_name character varying(100) NOT NULL,
    icon_skill character varying(200),
    short_desc text,
    proficiency integer,
    category character varying(50),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

CREATE TABLE public."user" (
    id bigint NOT NULL DEFAULT nextval('public.user_id_seq'::regclass),
    username character varying(80) NOT NULL,
    email character varying(120) NOT NULL,
    password text NOT NULL,
    role character varying(20),
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);

-- ============================================
-- ADD PRIMARY KEYS AND CONSTRAINTS
-- ============================================

ALTER TABLE ONLY public.about
    ADD CONSTRAINT about_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);

ALTER TABLE ONLY public.contact
    ADD CONSTRAINT contact_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.experience
    ADD CONSTRAINT experience_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.menu
    ADD CONSTRAINT menu_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.project
    ADD CONSTRAINT project_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.skill
    ADD CONSTRAINT skill_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);

-- ============================================
-- SET SEQUENCE OWNERSHIP
-- ============================================

ALTER SEQUENCE public.about_id_seq OWNED BY public.about.id;
ALTER SEQUENCE public.contact_id_seq OWNED BY public.contact.id;
ALTER SEQUENCE public.experience_id_seq OWNED BY public.experience.id;
ALTER SEQUENCE public.menu_id_seq OWNED BY public.menu.id;
ALTER SEQUENCE public.project_id_seq OWNED BY public.project.id;
ALTER SEQUENCE public.skill_id_seq OWNED BY public.skill.id;
ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;

-- ============================================
-- INSERT DATA
-- ============================================

-- Insert data into about table
INSERT INTO public.about (id, title, content, image, created_at, updated_at) VALUES
(1, 'About;Introduction;About Me', 'Hi, I''m Mang Bao — a passionate Frontend Developer with over 3 years of experience in building and maintaining modern web applications. I graduated from Nha Trang University with a degree in Software Technology and have been deeply involved in both UI/UX development and backend integration ever since.; Throughout my career, I''ve contributed to various projects at companies like Gravity Global, TMA Solutions, and LTV Software, where I worked on frontend development, API integration, performance optimization, and bug fixing. I''ve also actively collaborated with teams to address user feedback and deliver projects efficiently.;Currently, I''m continuing to sharpen my skills in both frontend and backend development, while also exploring DevOps. My long-term goal is to become a skilled Fullstack Developer who can take ownership of end-to-end product development and bring lasting value to the team and company.', 'square-avt_glko8i', NULL, NULL);

-- Insert data into alembic_version table
INSERT INTO public.alembic_version (version_num) VALUES
('1d5290139167');

-- Insert data into contact table
-- (No data in backup)

-- Insert data into experience table
INSERT INTO public.experience (id, company_name, role_name, desc_role, company_location, start_date, end_date, is_current, created_at, updated_at) VALUES
(3, 'TMA Solutions Binh Dinh', 'auto', 'Install automation framework for project, and write automation scripts based on testers'' test cases. Join the company_name''s training team for interns.', NULL, '20220701', '20240301', false, '2025-06-06 00:00:00', '2025-06-06 00:00:00'),
(4, 'Gravity Vietnam', 'fe', 'Develop sophisticated, animated, responsive and adaptive websites using HTML5, CSS, jQuery, Tailwind CSS, Laravel, PHP, MySQL, SEO; for all browsers, optimized for desktop, notebook, smartphones and tablets (iOS, Android, Windows).', NULL, '20220101', '20220401', false, '2025-06-06 00:00:00', '2025-06-06 00:00:00'),
(2, 'TMA Solutions Binh Dinh', 'fe, be', 'Develop system websites to manage network status, IPs, DNS, Servers and provide warnings. Website management uses Python, Flask Framework, RESTful API, ReactJS, Material-UI, Cassandra, and Docker.', NULL, '20220701', '20240301', false, '2025-06-06 00:00:00', '2025-06-06 00:00:00'),
(1, 'LTV Software', 'fe, be', 'Involved in full-cycle web development: building UI and APIs, fixing bugs. Optimizing performance, and improving UX. Collaborated with the team lead to address customer feedback and implement solutions.', NULL, '20240301', NULL, true, '2025-06-06 00:00:00', '2025-06-06 00:00:00');

-- Insert data into menu table
INSERT INTO public.menu (id, title, menu_name, menu_url, menu_order, is_active, created_at, updated_at) VALUES
(1, 'About;Introduction;About Me', 'About', '#about', NULL, true, '2025-06-05 22:47:17', '2025-06-05 22:47:22'),
(2, 'Projects;What I have done so far', 'Projects', '#projects', NULL, true, '2025-06-05 22:47:50', '2025-06-05 22:47:53'),
(3, 'Skills;What I do', 'Skills', '#skills', NULL, true, '2025-06-05 22:48:56', '2025-06-05 22:49:00'),
(4, 'Experiences;Where I do', 'Experiences', '#experiences', NULL, true, '2025-06-05 22:49:39', '2025-06-05 22:49:42'),
(5, 'Contact;Get in touch', 'Contact', '#contact', NULL, true, '2025-06-05 22:50:02', '2025-06-05 22:50:06');

-- Insert data into project table
INSERT INTO public.project (id, title, image, description, role, project_url, github_url, technologies, start_date, end_date, created_at, updated_at) VALUES
(1, 'Hi-Navi Vessel Management Service', 'MenloSecurity_Logo1_pscs6o', 'The HVMS web application helps manage materials, personnel, procurement processes,... for both shore-based and vessel-based operations. The project consists of three teams: Biz 1, Biz 2, and Common. My team, Biz 1, is responsible for implementing the Procurement module. As a front-end developer, I develop and maintain various procurement-related features.', 'Developed and optimized front-end features for procurement modules.; Collaborated cross-functionally to integrate systems and enhance UI/UX based on user feedback.; Maintained documentation for new features.', 'xxx', 'xxx', 'VueJS, Typescript, Vite, Yarn Tailwind CSS, Micro-FrontEnd, Pinia Store, Java, Kainos Framework, PostgresSQL', '20240301', 'Present', NULL, NULL),
(2, 'Menlo Security', 'MenloSecurity_Logo1_pscs6o', 'Menlo Security provides a cloud-based isolation platform to protect organizations from cyber threats by isolating harmful web elements. The platform acts like a gate, scanning and redirecting internet traffic to secure websites. I have the Automation Tester role involves testing new features and using automation tests for existing functions.', 'Test future; code automation to test old function.', 'xxx', 'xxx', 'Python, Robot Framework, Selenium.', '20231101', '20240301', NULL, NULL),
(3, 'Bluecat Health Monitoring', 'bluecat_health_monitoring_website_image1_ifftvi', 'The web application assists companies in overseeing server infrastructure on virtual machines (VMs), focusing on monitoring and optimizing the performance of BlueCat DNS/DHCP Server (BDDS) servers. It offers system information using graphs and alerts users about server issues. Developer responsibilities encompass API creation, enhancing back-end functionality, resolve front-end UI errors, and automating setup and code based on tester test cases.', 'Maintenance, develop UI/UX; Write API in Back-End; Test and bug fixing, review code UI; Setup and code automation by test case.', 'xxx', 'xxx', 'Python, Flask Framework, RESTful API, ReactJS, Material-UI, Robot Framework, Cassandra, Docker.', '20220101', '20231001', NULL, NULL),
(4, 'Pecan Deluxe', 'pecan-deluxe-share1_uub6vg', 'The web application serves Pecan Deluxe, a confectionery company, enabling users to browse and order products while providing essential product details. Website managers have control over product display, order tracking, and customer feedback. The developer focuses on coding UI modules and addressing both front-end and back-end issues.', 'Develop UI/UX; Unit test, fix bugs in Front-end and Back-end; Design website modules following architecture.', 'https://pecandeluxe.com', 'xxx', 'JQuery, PHP, Laravel framework, Tailwind CSS, SEO, MySQL.', '20220114', '20220401', NULL, NULL),
(5, 'Nha Trang University Exam Schedule', 'ntu-bg_se89p1', 'Building a website to support automatic exam scheduling for Nha Trang University. Allows students to view exam schedules, register for exam schedules, view news, etc. Faculty teachers can view and set automatic/manual exam schedules and export exam schedules to Excel. Manage exam schedules by each department, and support students to communicate directly with each other on the website to grasp and arrange time together more effectively.', 'Maintenance, develop UI/UX Homepage, Admin, and all function; Code the functions in BE; Fix bug and Report', 'https://github.com/MangBao/doantotnghiep2022', 'xxx', 'PHP, Laravel Framework, Tailwind CSS, MySQL.', '20220401', '20220601', NULL, NULL),
(6, 'Homita milk tea shop', 'homita_bg_ky4aqi', 'Building a website to manage the Homita milk tea shop according to the MVC model. Allows ordering milk tea online via the shopping cart, displaying new items, and sending feedback. CRUD bills, drinks, staff... ', 'Code the functions of invoice management, feedback management, and sending feedback in BE; Setup folder and project files according to the MVC model', 'https://github.com/60-CNPM-OpenSourceGroup/QuanLyTraSua-PHP-MVC', 'xxx', 'PHP, Javascript, MVC, Bootstrap, MySQL.', '20211101', '20211130', NULL, NULL);

-- Insert data into skill table
INSERT INTO public.skill (id, skill_name, icon_skill, short_desc, proficiency, category, created_at, updated_at) VALUES
(1, 'HTML', 'html_h9ssbm', 'I have a strong command of HTML for organizing web pages and generating meaningful content that can be accessed by all users.', NULL, NULL, NULL, NULL),
(2, 'CSS', 'css_lgzxuc', 'I possess expertise in utilizing CSS to design web pages and craft visually captivating layouts that enhance the overall user experience.', NULL, NULL, NULL, NULL),
(3, 'Material UI', 'mui_beyvma', 'I have expertise in using Material UI to design website interfaces, ensuring the best user experience.', NULL, NULL, NULL, NULL),
(4, 'Tailwind CSS', 'tailwindcss_uzirkz', 'I have experience using TailwindCSS to design website interfaces, ensure website performance, and user experience.', NULL, NULL, NULL, NULL),
(5, 'JavaScript', 'javascript_gqiexu', 'I have substantial experience in employing JavaScript to introduce interactivity and functionality into web pages, resulting in dynamic user interfaces.', NULL, NULL, NULL, NULL),
(6, 'ReactJS', 'reactjs_ekorv8', 'I am well-versed in React, proficient in creating reusable components and managing application state using hooks and context.', NULL, NULL, NULL, NULL),
(7, 'Redux Toolkit', 'redux_vfyxuu', 'In my React application, I used Redux Toolkit to manage the state of the application. I created slices, actions, and reducers to manage data and improve application performance.', NULL, NULL, NULL, NULL),
(8, 'Git', 'git_qwhfa5', 'I am proficient in Git, managing code changes, collaborating with others, and resolving conflicts effectively.', NULL, NULL, NULL, NULL),
(9, 'GitHub', 'github_txzruj', 'I am skilled in using GitHub for seamless project collaboration, code sharing, and issue tracking. Through GitHub, I efficiently create and manage repositories and effectively present my work to potential employers.', NULL, NULL, NULL, NULL),
(10, 'Python', 'py_msu4lr', 'With 2 years of Python experience, I am adept at coding functions and creating API using Flask.', NULL, NULL, NULL, NULL),
(11, 'Flask', 'flask_qwvsqu', 'With 1.5 years of experience in Flask, I am proficient in the process of creating APIs, support functions and working on this framework.', NULL, NULL, NULL, NULL),
(12, 'Cassandra', 'cassandra_fvd8te', 'In a project using Cassandra, I am familiar with data queries, ensuring product performance throughout the operation.', NULL, NULL, NULL, NULL),
(13, 'Eslint', 'eslint_a0l4ui', 'I utilize ESLint to identify and resolve code issues, as well as standardize the structure of my projects. With ESLint, I ensure code quality and consistency throughout my development process.', NULL, NULL, NULL, NULL),
(14, 'Responsive Design', 'responsive_design_ozkj5z', 'I am proficient in Responsive Design, I created a user interface that''s compatible with various screen sizes through flexible CSS, media queries, and extensive testing with tools like DevTools.', NULL, NULL, NULL, NULL),
(15, 'Docker', 'docker_tb7aqw', 'I have experience working with Docker to deploy applications, I am also familiar with Docker commands and using Docker Compose to manage multiple containers at once.', NULL, NULL, NULL, NULL),
(16, 'Robot Framework', 'robot_framework_hxnaqk', 'I have 9 months of experience working with Robot Framework, I have developed and deployed automated test suites for web applications based on Manual Tester test cases. This experience helps me improve product quality and reduce manual testing time.', NULL, NULL, NULL, NULL),
(17, 'Ubuntu', 'ubuntu_vwhyqz', 'While using Ubuntu, I installed, configured, and managed web servers and systems, and I''m adept at command line operations, including SSH, apt, and systemd for system maintenance.', NULL, NULL, NULL, NULL),
(18, 'Laravel', 'laravel_msn2nq', 'In a project using Laravel, I developed web applications. I worked with routing, middleware, authentication, and Eloquent ORM.', NULL, NULL, NULL, NULL),
(19, 'MySQL', 'mysql_xprlq8', 'My experience with MySQL includes database design, SQL query optimization, and MySQL server deployment, ensuring database reliability and performance.', NULL, NULL, NULL, NULL),
(20, 'Selenium', 'selenium_ynuwas', 'I used Selenium to write automated scripts for cross-browser UI testing, becoming proficient with Selenium APIs and ensuring application stability and quality through automated testing.', NULL, NULL, NULL, NULL),
(21, 'Jira', 'jira_e8ngta', 'In project management, I used Jira to track work. I have become familiar with creating and managing user stories, tasks, and sprints in Jira to ensure work is completed on time.', NULL, NULL, NULL, NULL),
(22, 'SEO', 'seo_y3fvzp.png', 'In SEO skills, I optimized websites to increase rankings on search engines. I performed an SEO audit, optimized content, and built links to the site.', NULL, NULL, NULL, NULL);

-- Insert data into user table
INSERT INTO public."user" (id, username, email, password, role, created_at, updated_at) VALUES
(2, 'mbao1301', 'mbao1301@gmail.com', 'scrypt:32768:8:1$IZzT3VPigfy1OMKz$d6840fa2c48ba387ed14b3f3d849a74beadbda142451311f8b07744ae0b8094eb9a045f86aba77d927088bdeffc5d03972157dfbf3bfbf7857cd92b2a91b134c', 'user', '2025-06-05 23:22:03.879948', NULL);

-- ============================================
-- SET SEQUENCE VALUES
-- ============================================

SELECT pg_catalog.setval('public.about_id_seq', 1, true);
SELECT pg_catalog.setval('public.contact_id_seq', 1, false);
SELECT pg_catalog.setval('public.experience_id_seq', 1, false);
SELECT pg_catalog.setval('public.menu_id_seq', 1, false);
SELECT pg_catalog.setval('public.project_id_seq', 6, true);
SELECT pg_catalog.setval('public.skill_id_seq', 22, true);
SELECT pg_catalog.setval('public.user_id_seq', 1, false);

-- ============================================
-- CREATE INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================
-- Indexes for frequently queried columns to improve query performance

-- Indexes for Contact table
CREATE INDEX IF NOT EXISTS idx_contact_status ON public.contact(status);
CREATE INDEX IF NOT EXISTS idx_contact_created_at ON public.contact(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contact_status_created_at ON public.contact(status, created_at DESC);

-- Indexes for Project table
CREATE INDEX IF NOT EXISTS idx_project_start_date ON public.project(start_date DESC);
CREATE INDEX IF NOT EXISTS idx_project_created_at ON public.project(created_at DESC);

-- Indexes for Experience table
CREATE INDEX IF NOT EXISTS idx_experience_start_date ON public.experience(start_date DESC);
CREATE INDEX IF NOT EXISTS idx_experience_is_current ON public.experience(is_current) WHERE is_current = true;
CREATE INDEX IF NOT EXISTS idx_experience_created_at ON public.experience(created_at DESC);

-- Indexes for Skill table
CREATE INDEX IF NOT EXISTS idx_skill_category ON public.skill(category);
CREATE INDEX IF NOT EXISTS idx_skill_category_proficiency ON public.skill(category, proficiency DESC);

-- Indexes for Menu table
CREATE INDEX IF NOT EXISTS idx_menu_is_active ON public.menu(is_active) WHERE is_active = true;
CREATE INDEX IF NOT EXISTS idx_menu_order ON public.menu(menu_order ASC);

-- Indexes for User table (already has unique indexes on username and email)
CREATE INDEX IF NOT EXISTS idx_user_email ON public."user"(email);
CREATE INDEX IF NOT EXISTS idx_user_created_at ON public."user"(created_at DESC);

-- Composite index for common query patterns
CREATE INDEX IF NOT EXISTS idx_contact_status_created_at_composite ON public.contact(status, created_at DESC);

-- Note: These indexes will slightly slow down INSERT/UPDATE operations
-- but significantly speed up SELECT queries, especially with WHERE and ORDER BY clauses

-- ============================================
-- END OF SCRIPT
-- ============================================

