--
-- PostgreSQL database dump
--

\restrict JDUKtL4hfoh3XNrbgguV5CqpwmKipHGqXuQVLvXnbpqLJRoVGP80cBAJ7eT2VeX

-- Dumped from database version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.20 (Ubuntu 14.20-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: decisionai_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO decisionai_user;

--
-- Name: task_history; Type: TABLE; Schema: public; Owner: decisionai_user
--

CREATE TABLE public.task_history (
    id integer NOT NULL,
    task_id character varying(36) NOT NULL,
    user_id character varying(36) NOT NULL,
    action character varying(50) NOT NULL,
    changes json,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.task_history OWNER TO decisionai_user;

--
-- Name: task_history_id_seq; Type: SEQUENCE; Schema: public; Owner: decisionai_user
--

CREATE SEQUENCE public.task_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_history_id_seq OWNER TO decisionai_user;

--
-- Name: task_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: decisionai_user
--

ALTER SEQUENCE public.task_history_id_seq OWNED BY public.task_history.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: decisionai_user
--

CREATE TABLE public.tasks (
    id character varying(36) NOT NULL,
    user_id character varying(36) NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    category character varying(50),
    tags json,
    priority integer,
    impact integer,
    complexity integer,
    estimated_hours double precision,
    status character varying(20),
    progress integer,
    due_date timestamp without time zone NOT NULL,
    completed_at timestamp without time zone,
    ai_insights json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    started_at timestamp without time zone
);


ALTER TABLE public.tasks OWNER TO decisionai_user;

--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: decisionai_user
--

CREATE TABLE public.user_preferences (
    id integer NOT NULL,
    user_id character varying(36),
    theme character varying(20),
    notifications json,
    ai_settings json,
    display_settings json
);


ALTER TABLE public.user_preferences OWNER TO decisionai_user;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: decisionai_user
--

CREATE SEQUENCE public.user_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_preferences_id_seq OWNER TO decisionai_user;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: decisionai_user
--

ALTER SEQUENCE public.user_preferences_id_seq OWNED BY public.user_preferences.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: decisionai_user
--

CREATE TABLE public.users (
    id character varying(36) NOT NULL,
    email character varying(120) NOT NULL,
    username character varying(80),
    password_hash character varying(128) NOT NULL,
    name character varying(100) NOT NULL,
    is_active boolean,
    is_verified boolean,
    role character varying(20),
    preferences json,
    stats json,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    last_login timestamp without time zone
);


ALTER TABLE public.users OWNER TO decisionai_user;

--
-- Name: task_history id; Type: DEFAULT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.task_history ALTER COLUMN id SET DEFAULT nextval('public.task_history_id_seq'::regclass);


--
-- Name: user_preferences id; Type: DEFAULT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN id SET DEFAULT nextval('public.user_preferences_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: decisionai_user
--

COPY public.alembic_version (version_num) FROM stdin;
\.


--
-- Data for Name: task_history; Type: TABLE DATA; Schema: public; Owner: decisionai_user
--

COPY public.task_history (id, task_id, user_id, action, changes, "timestamp") FROM stdin;
1	6a3f7c1b-699e-4816-9099-6da9455e9170	801690ca-ff26-40f4-aedf-9df316dd19ea	created	{"from": null, "to": {"id": "6a3f7c1b-699e-4816-9099-6da9455e9170", "title": "1 Complete API Documentation", "description": "Create comprehensive API documentation for all endpoints", "category": "Documentation", "tags": ["api", "documentation", "important"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 4.5, "status": "pending", "progress": 0, "due_date": "2026-02-15T23:59:59+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 7.398850664903059, "suggested_resources": ["Documentation", "Research"], "complexity_score": 4, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9142670336526766, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 2}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 7}}	2026-02-08 10:06:55.563282
2	8b30bf05-4e73-477d-b1bf-dcf714599738	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	created	{"from": null, "to": {"id": "8b30bf05-4e73-477d-b1bf-dcf714599738", "title": "123", "description": "qwer", "category": "Health", "tags": [], "priority": 3, "impact": 5, "complexity": 3, "estimated_hours": 1.0, "status": "pending", "progress": 0, "due_date": "2026-02-18T00:00:00+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 5.337586918195311, "suggested_resources": ["Documentation", "Research"], "complexity_score": 3, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.8230199710939262, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 0}, "user_id": "42d4a5e9-0f84-4bdb-b18e-066166d3aa27", "is_overdue": false, "task_score": 3.5999999999999996, "days_until_due": 9}}	2026-02-08 10:19:02.371892
3	a9611b53-cadf-4e23-9af3-81802b565b58	801690ca-ff26-40f4-aedf-9df316dd19ea	created	{"from": null, "to": {"id": "a9611b53-cadf-4e23-9af3-81802b565b58", "title": "1 Complete API Documentation", "description": "Create comprehensive API documentation for all endpoints", "category": "Documentation", "tags": ["api", "documentation", "important"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 4.5, "status": "pending", "progress": 0, "due_date": "2026-02-15T23:59:59+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 1.163505151134409, "suggested_resources": ["Documentation", "Research"], "complexity_score": 1, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9404529823636811, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 1}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 7}}	2026-02-08 10:36:26.004668
4	6a3f7c1b-699e-4816-9099-6da9455e9170	801690ca-ff26-40f4-aedf-9df316dd19ea	updated	{"from": {"id": "6a3f7c1b-699e-4816-9099-6da9455e9170", "title": "1 Complete API Documentation", "description": "Create comprehensive API documentation for all endpoints", "category": "Documentation", "tags": ["api", "documentation", "important"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 4.5, "status": "pending", "progress": 0, "due_date": "2026-02-16T02:59:59", "completed_at": null, "created_at": "2026-02-08T13:06:55.340680", "updated_at": "2026-02-08T13:06:55.340702", "started_at": null, "ai_insights": {"estimated_completion_time": 7.398850664903059, "suggested_resources": ["Documentation", "Research"], "complexity_score": 4, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9142670336526766, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 2}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 7}, "to": {"id": "6a3f7c1b-699e-4816-9099-6da9455e9170", "title": "Test Task", "description": "Test description", "category": "Testing", "tags": ["test"], "priority": 2, "impact": 5, "complexity": 2, "estimated_hours": 2.0, "status": "pending", "progress": 0, "due_date": "2026-02-15T23:59:59+00:00", "completed_at": null, "created_at": "2026-02-08T13:06:55.340680", "updated_at": "2026-02-08T10:43:53.231760", "started_at": null, "ai_insights": {"estimated_completion_time": 4.032564343701006, "suggested_resources": ["Documentation", "Research"], "complexity_score": 4, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9423906686390581, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 3}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 2.9000000000000004, "days_until_due": 7}}	2026-02-08 10:43:53.258014
5	8b30bf05-4e73-477d-b1bf-dcf714599738	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	updated	{"from": {"id": "8b30bf05-4e73-477d-b1bf-dcf714599738", "title": "123", "description": "qwer", "category": "Health", "tags": [], "priority": 3, "impact": 5, "complexity": 3, "estimated_hours": 1.0, "status": "pending", "progress": 0, "due_date": "2026-02-18T03:00:00", "completed_at": null, "created_at": "2026-02-08T13:19:02.363581", "updated_at": "2026-02-08T13:19:02.363593", "started_at": null, "ai_insights": {"estimated_completion_time": 5.337586918195311, "suggested_resources": ["Documentation", "Research"], "complexity_score": 3, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.8230199710939262, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 0}, "user_id": "42d4a5e9-0f84-4bdb-b18e-066166d3aa27", "is_overdue": false, "task_score": 3.5999999999999996, "days_until_due": 9}, "to": {"id": "8b30bf05-4e73-477d-b1bf-dcf714599738", "title": "123", "description": "qwerty", "category": "Health", "tags": [], "priority": 3, "impact": 5, "complexity": 3, "estimated_hours": 1.0, "status": "pending", "progress": 0, "due_date": "2026-02-18T00:00:00+00:00", "completed_at": null, "created_at": "2026-02-08T13:19:02.363581", "updated_at": "2026-02-08T10:44:10.426924", "started_at": null, "ai_insights": {"estimated_completion_time": 9.761125525365738, "suggested_resources": ["Documentation", "Research"], "complexity_score": 5, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.789779520783115, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 2}, "user_id": "42d4a5e9-0f84-4bdb-b18e-066166d3aa27", "is_overdue": false, "task_score": 3.5999999999999996, "days_until_due": 9}}	2026-02-08 10:44:10.43179
6	a9611b53-cadf-4e23-9af3-81802b565b58	801690ca-ff26-40f4-aedf-9df316dd19ea	updated	{"from": {"id": "a9611b53-cadf-4e23-9af3-81802b565b58", "title": "1 Complete API Documentation", "description": "Create comprehensive API documentation for all endpoints", "category": "Documentation", "tags": ["api", "documentation", "important"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 4.5, "status": "pending", "progress": 0, "due_date": "2026-02-16T02:59:59", "completed_at": null, "created_at": "2026-02-08T13:36:25.988539", "updated_at": "2026-02-08T13:36:25.988553", "started_at": null, "ai_insights": {"estimated_completion_time": 1.163505151134409, "suggested_resources": ["Documentation", "Research"], "complexity_score": 1, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9404529823636811, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 1}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 7}, "to": {"id": "a9611b53-cadf-4e23-9af3-81802b565b58", "title": "1 Complete API Documentation", "description": "Create comprehensive API documentation for all endpoints", "category": "Documentation", "tags": ["api", "documentation", "important"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 5.0, "status": "pending", "progress": 0, "due_date": "2026-02-16T00:00:00+00:00", "completed_at": null, "created_at": "2026-02-08T13:36:25.988539", "updated_at": "2026-02-08T12:16:21.319846", "started_at": null, "ai_insights": {"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 7}}	2026-02-08 12:16:21.493917
7	3e6e56dd-c086-420c-9604-f1fc59147859	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	created	{"from": null, "to": {"id": "3e6e56dd-c086-420c-9604-f1fc59147859", "title": "dfgh", "description": "sdfg", "category": "Work", "tags": ["d"], "priority": 3, "impact": 5, "complexity": 3, "estimated_hours": 1.0, "status": "pending", "progress": 0, "due_date": "2026-02-18T00:00:00+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}, "user_id": "42d4a5e9-0f84-4bdb-b18e-066166d3aa27", "is_overdue": false, "task_score": 3.5999999999999996, "days_until_due": 8}}	2026-02-09 19:43:24.792044
8	9e5f031d-89f3-4715-84c5-b46b82976156	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	created	{"from": null, "to": {"id": "9e5f031d-89f3-4715-84c5-b46b82976156", "title": "dfgh", "description": "sdfg", "category": "Work", "tags": ["sdf"], "priority": 3, "impact": 5, "complexity": 3, "estimated_hours": 1.0, "status": "pending", "progress": 0, "due_date": "2026-02-17T00:00:00+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}, "user_id": "42d4a5e9-0f84-4bdb-b18e-066166d3aa27", "is_overdue": false, "task_score": 3.5999999999999996, "days_until_due": 7}}	2026-02-09 19:44:26.905129
9	26d6df87-0a83-455e-9608-14af94ea551b	801690ca-ff26-40f4-aedf-9df316dd19ea	created	{"from": null, "to": {"id": "26d6df87-0a83-455e-9608-14af94ea551b", "title": "qwerty", "description": "1234567", "category": "Other", "tags": ["qwerty"], "priority": 4, "impact": 8, "complexity": 4, "estimated_hours": 4.0, "status": "in-progress", "progress": 0, "due_date": "2026-03-03T00:00:00+00:00", "completed_at": null, "created_at": null, "updated_at": null, "started_at": null, "ai_insights": {"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 5.2, "days_until_due": 13}}	2026-02-17 14:16:03.3671
10	36a96a51-b06e-4111-9884-a98a4ad30d08	801690ca-ff26-40f4-aedf-9df316dd19ea	updated	{"from": {"id": "36a96a51-b06e-4111-9884-a98a4ad30d08", "title": "Plan Summer Europe Trip", "description": "Plan 2-week trip to Europe visiting Paris, Rome, and Barcelona. Research flights, accommodations, activities, transportation between cities, and create daily itinerary.", "category": "Travel", "tags": ["vacation", "travel", "europe", "planning"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 10.0, "status": "in-progress", "progress": 60, "due_date": "2026-05-01T23:59:59", "completed_at": null, "created_at": "2026-01-29T16:11:13.130219", "updated_at": "2026-02-08T16:11:13.130219", "started_at": null, "ai_insights": {"complexity_score": 3, "estimated_completion_time": 12.0, "potential_blockers": ["Budget constraints", "Booking availability", "Itinerary optimization"], "recommended_approach": "Book flights early, use travel apps, create flexible itinerary", "suggested_resources": ["Travel websites", "Booking apps", "Travel guides"]}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 73}, "to": {"id": "36a96a51-b06e-4111-9884-a98a4ad30d08", "title": "Plan Summer Europe Trip", "description": "Plan 2-week trip to Europe visiting Paris, Rome, and Barcelona. Research flights, accommodations, activities, transportation between cities, and create daily itinerary.", "category": "Travel", "tags": ["vacation", "travel", "europe", "planning"], "priority": 2, "impact": 8, "complexity": 3, "estimated_hours": 10.0, "status": "in-progress", "progress": 60, "due_date": "2026-05-01T00:00:00+00:00", "completed_at": null, "created_at": "2026-01-29T16:11:13.130219", "updated_at": "2026-02-17T14:17:03.559882", "started_at": null, "ai_insights": {"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}, "user_id": "801690ca-ff26-40f4-aedf-9df316dd19ea", "is_overdue": false, "task_score": 3.8999999999999995, "days_until_due": 72}}	2026-02-17 14:17:03.56615
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: decisionai_user
--

COPY public.tasks (id, user_id, title, description, category, tags, priority, impact, complexity, estimated_hours, status, progress, due_date, completed_at, ai_insights, created_at, updated_at, started_at) FROM stdin;
6a3f7c1b-699e-4816-9099-6da9455e9170	801690ca-ff26-40f4-aedf-9df316dd19ea	Test Task	Test description	Testing	["test"]	2	5	2	2	pending	0	2026-02-16 02:59:59	\N	{"estimated_completion_time": 4.032564343701006, "suggested_resources": ["Documentation", "Research"], "complexity_score": 4, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.9423906686390581, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 3}	2026-02-08 13:06:55.34068	2026-02-08 10:43:53.23176	\N
8b30bf05-4e73-477d-b1bf-dcf714599738	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	123	qwerty	Health	[]	3	5	3	1	pending	0	2026-02-18 03:00:00	\N	{"estimated_completion_time": 9.761125525365738, "suggested_resources": ["Documentation", "Research"], "complexity_score": 5, "recommended_approach": "Break into smaller subtasks", "confidence_score": 0.789779520783115, "potential_blockers": ["Lack of information", "Dependencies"], "similar_tasks_completed": 2}	2026-02-08 13:19:02.363581	2026-02-08 10:44:10.426924	\N
a9611b53-cadf-4e23-9af3-81802b565b58	801690ca-ff26-40f4-aedf-9df316dd19ea	1 Complete API Documentation	Create comprehensive API documentation for all endpoints	Documentation	["api", "documentation", "important"]	2	8	3	5	pending	0	2026-02-16 03:00:00	\N	{"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}	2026-02-08 13:36:25.988539	2026-02-08 12:16:21.319846	\N
e66a9c4c-d8bb-4edc-8b70-49a10d2caa67	801690ca-ff26-40f4-aedf-9df316dd19ea	Build Machine Learning Model for Customer Segmentation	Develop a clustering algorithm using K-means and DBSCAN to segment customers based on purchasing behavior, demographics, and engagement metrics. Need to collect data from multiple sources (CRM, web analytics, transaction database), perform data cleaning and preprocessing, feature engineering, train multiple models, evaluate using silhouette score and Davies-Bouldin index, and visualize results using PCA and t-SNE.	AI/ML	["machine-learning", "python", "clustering", "data-science", "scikit-learn"]	1	9	5	35	in-progress	40	2026-03-10 23:59:59	\N	{"complexity_score": 5, "estimated_completion_time": 42.5, "potential_blockers": ["Data quality issues", "Computational resources", "Feature selection"], "recommended_approach": "Start with exploratory data analysis, then prototype with smaller dataset", "suggested_resources": ["Scikit-learn documentation", "Research papers on customer segmentation", "Cloud GPU instances"]}	2026-02-08 15:35:23.950339	2026-02-08 15:35:23.950339	\N
4976435e-2698-4110-9b6a-a9cac45adb8a	801690ca-ff26-40f4-aedf-9df316dd19ea	Build ML Model for Fraud Detection	Develop a machine learning model using Python, TensorFlow, and Scikit-learn to detect fraudulent transactions. Need to collect historical data, perform feature engineering, train models (logistic regression, random forest, neural networks), and deploy as a microservice.	AI/ML	["machine-learning", "python", "fraud-detection", "tensorflow"]	1	9	5	40	in-progress	30	2026-03-15 23:59:59	\N	{"complexity_score": 5, "estimated_completion_time": 45.5, "potential_blockers": ["Data quality", "Model interpretability", "Deployment infrastructure"], "recommended_approach": "Start with exploratory analysis, then iterative model development", "suggested_resources": ["TensorFlow documentation", "Fraud detection research papers", "Cloud ML platforms"]}	2026-02-08 15:37:35.762098	2026-02-08 15:37:35.762098	\N
a0d1811a-2377-4d10-a7e5-bd41a3fb2309	801690ca-ff26-40f4-aedf-9df316dd19ea	Database Migration to PostgreSQL	Migrate production database from MySQL to PostgreSQL. Currently blocked waiting for security approval and maintenance window scheduling.	DevOps	["database", "migration", "postgresql", "blocked"]	2	8	4	24	blocked	15	2026-02-25 23:59:59	\N	{"complexity_score": 4, "estimated_completion_time": 28.0, "potential_blockers": ["Security approvals", "Downtime constraints", "Data integrity"], "recommended_approach": "Plan phased migration with rollback strategy", "suggested_resources": ["Migration tools", "PostgreSQL documentation", "Backup strategies"]}	2026-02-08 15:37:35.769117	2026-02-08 15:37:35.769117	\N
16aa6afd-3aa3-4603-a476-a895fdf6cc8d	801690ca-ff26-40f4-aedf-9df316dd19ea	Fix CSS Responsive Layout	Fixed mobile layout issues on dashboard page. Updated CSS media queries and flexbox alignment.	Frontend	["css", "responsive", "bug", "mobile"]	3	5	2	3	completed	100	2026-02-10 23:59:59	2026-02-08 14:30:00	{"complexity_score": 2, "estimated_completion_time": 3.5, "potential_blockers": ["Browser compatibility", "Testing devices"], "recommended_approach": "Implemented successfully", "suggested_resources": ["CSS grid documentation", "Browser dev tools"], "actual_completion_time": 2.8}	2026-02-05 09:00:00	2026-02-08 14:30:00	2026-02-05 09:30:00
2c4d8cda-f2a8-4326-9086-fe1ad36865db	801690ca-ff26-40f4-aedf-9df316dd19ea	Emergency SQL Injection Fix	Critical security vulnerability found. Need to patch SQL injection in user search API immediately.	Security	["security", "urgent", "sql-injection", "hotfix"]	1	10	3	6	in-progress	70	2026-02-09 18:00:00	\N	{"complexity_score": 3, "estimated_completion_time": 8.0, "potential_blockers": ["Testing time", "Deployment coordination"], "recommended_approach": "Immediate parameterized query implementation", "suggested_resources": ["OWASP guide", "Security scanning tools"]}	2026-02-08 12:37:35.778078	2026-02-08 15:37:35.778078	\N
6f7d6af6-27b3-4c97-80d9-8a95323cab2e	801690ca-ff26-40f4-aedf-9df316dd19ea	Complete API Documentation	Create comprehensive API documentation using OpenAPI/Swagger. Document 50+ endpoints with examples, error codes, and authentication methods.	Documentation	["api", "documentation", "swagger", "openapi"]	2	7	3	15	pending	0	2026-02-28 23:59:59	\N	{"complexity_score": 3, "estimated_completion_time": 18.0, "potential_blockers": ["Endpoint changes", "Example data"], "recommended_approach": "Start with high-priority endpoints first", "suggested_resources": ["OpenAPI specification", "Swagger UI", "Postman"]}	2026-02-08 15:37:35.787205	2026-02-08 15:37:35.787205	\N
5ea7bfdb-f4c2-4e42-a1cf-fa942acfcf0f	801690ca-ff26-40f4-aedf-9df316dd19ea	Design 4-Week Workout Program	Create a balanced workout routine focusing on strength training 3x/week, cardio 2x/week, and flexibility 1x/week. Include specific exercises, sets, reps, and rest periods. Need to consider current fitness level and available equipment (dumbbells, resistance bands, yoga mat).	Health	["workout", "fitness", "routine", "exercise"]	2	8	3	5	pending	0	2026-02-20 23:59:59	\N	{"complexity_score": 3, "estimated_completion_time": 6.0, "potential_blockers": ["Equipment availability", "Time commitment assessment", "Fitness level evaluation"], "recommended_approach": "Start with basic compound movements, then add accessory exercises", "suggested_resources": ["Fitness apps", "Exercise form videos", "Workout tracking spreadsheet"]}	2026-02-08 16:09:52.121187	2026-02-08 16:09:52.121187	\N
2e1af770-bd8a-48f6-8632-7b3c8e7b9533	801690ca-ff26-40f4-aedf-9df316dd19ea	Weekly Healthy Meal Prep	Plan and prepare 7 days of balanced meals (breakfast, lunch, dinner) with 2000 calories/day target. Focus on protein-rich foods, complex carbs, and healthy fats. Need grocery list, recipes, and prep schedule.	Health	["meal-prep", "nutrition", "cooking", "health"]	3	7	2	4	in-progress	50	2026-02-11 18:00:00	\N	{"complexity_score": 2, "estimated_completion_time": 5.0, "potential_blockers": ["Grocery availability", "Cooking time", "Food preferences"], "recommended_approach": "Batch cook proteins and grains, assemble meals daily", "suggested_resources": ["Nutrition tracking app", "Recipe websites", "Meal prep containers"]}	2026-02-07 16:09:52.133823	2026-02-08 16:09:52.133823	\N
35f9a4ef-03e3-446f-8d39-d3111fabaade	801690ca-ff26-40f4-aedf-9df316dd19ea	Quarterly Investment Portfolio Analysis	Review current investment portfolio (stocks, bonds, ETFs, crypto). Analyze performance, rebalance allocations, research new opportunities, and update long-term financial goals. Need to consider risk tolerance and market conditions.	Finance	["investing", "portfolio", "finance", "analysis"]	2	9	4	8	pending	0	2026-03-31 23:59:59	\N	{"complexity_score": 4, "estimated_completion_time": 10.0, "potential_blockers": ["Market volatility", "Information overload", "Decision paralysis"], "recommended_approach": "Review one asset class at a time, compare against benchmarks", "suggested_resources": ["Financial news sites", "Portfolio tracking tools", "Investment research reports"]}	2026-02-08 16:10:11.414763	2026-02-08 16:10:11.414763	\N
fecb7b33-eb1b-4c22-90e9-8e00e210095d	801690ca-ff26-40f4-aedf-9df316dd19ea	Annual Tax Return Preparation	Gather all tax documents (W-2, 1099s, investment statements, receipts). Calculate deductions, complete tax forms, and file before deadline. Consider itemizing vs standard deduction.	Finance	["taxes", "finance", "deadline", "paperwork"]	1	8	3	12	in-progress	40	2026-04-15 23:59:59	\N	{"complexity_score": 3, "estimated_completion_time": 15.0, "potential_blockers": ["Missing documents", "Complex deductions", "Tax law changes"], "recommended_approach": "Organize documents first, use tax software, review carefully", "suggested_resources": ["Tax software", "IRS publications", "Receipt tracking app"]}	2026-02-05 16:10:11.422441	2026-02-08 16:10:11.422441	\N
8cd979dc-b002-4b19-9b02-a03f7f9385e7	801690ca-ff26-40f4-aedf-9df316dd19ea	Complete Machine Learning Course	Finish Coursera Machine Learning Specialization by Andrew Ng. Complete all programming assignments, quizzes, and final project. Currently on week 3 of 11.	Learning	["course", "machine-learning", "education", "skills"]	2	8	4	60	in-progress	25	2026-04-30 23:59:59	\N	{"complexity_score": 4, "estimated_completion_time": 70.0, "potential_blockers": ["Time commitment", "Complex concepts", "Programming challenges"], "recommended_approach": "Schedule regular study sessions, practice coding exercises", "suggested_resources": ["Course materials", "Online forums", "Practice datasets"]}	2026-01-15 10:00:00	2026-02-08 16:10:25.679642	2026-01-15 10:00:00
b2dea7b5-6128-4752-82d9-2ee4ae200eef	801690ca-ff26-40f4-aedf-9df316dd19ea	Read 12 Books This Year	Read one book per month across different genres: business, fiction, self-help, science. Current progress: 2 books completed. Need to select next books and maintain reading schedule.	Personal	["reading", "books", "learning", "goals"]	3	6	2	120	in-progress	16	2026-12-31 23:59:59	\N	{"complexity_score": 2, "estimated_completion_time": 150.0, "potential_blockers": ["Time management", "Book selection", "Reading consistency"], "recommended_approach": "Set weekly reading targets, keep book handy, join reading group", "suggested_resources": ["Book recommendations", "Audiobooks", "Reading tracker app"]}	2026-01-01 09:00:00	2026-02-08 16:10:25.684523	\N
4210a8f8-f95a-457d-bdbe-7f5ad4488cd8	801690ca-ff26-40f4-aedf-9df316dd19ea	Organize Home Office Space	Declutter and organize home office: sort paperwork, organize cables, setup ergonomic workstation, implement filing system, and create productive environment.	Home	["organization", "home", "productivity", "declutter"]	3	7	2	6	pending	0	2026-02-22 23:59:59	\N	{"complexity_score": 2, "estimated_completion_time": 8.0, "potential_blockers": ["Decision fatigue", "Space constraints", "Procrastination"], "recommended_approach": "Work in sections, use storage solutions, maintain regularly", "suggested_resources": ["Organizational tools", "Storage bins", "Digital filing system"]}	2026-02-08 16:10:43.798791	2026-02-08 16:10:43.798791	\N
74c1b378-c29f-467a-979f-9651f595825d	801690ca-ff26-40f4-aedf-9df316dd19ea	Spring Vegetable Garden Setup	Plan and plant spring vegetable garden. Research suitable plants for climate, prepare soil, create planting schedule, set up irrigation, and plan pest control.	Home	["garden", "plants", "outdoor", "sustainability"]	3	6	3	15	pending	10	2026-03-15 23:59:59	\N	{"complexity_score": 3, "estimated_completion_time": 20.0, "potential_blockers": ["Weather conditions", "Plant availability", "Pest issues"], "recommended_approach": "Start with easy vegetables, prepare soil early, monitor growth", "suggested_resources": ["Gardening books", "Planting calendar", "Soil testing kit"]}	2026-02-03 16:10:43.80193	2026-02-08 16:10:43.80193	\N
6053d6cc-ff1d-405e-a45f-5c57dbcc593e	801690ca-ff26-40f4-aedf-9df316dd19ea	AWS Solutions Architect Certification	Prepare for and pass AWS Solutions Architect Associate exam. Study all domains: design resilient architectures, define performant architectures, specify secure applications, design cost-optimized architectures.	Career	["certification", "aws", "cloud", "professional"]	1	9	4	80	in-progress	35	2026-05-31 23:59:59	\N	{"complexity_score": 4, "estimated_completion_time": 100.0, "potential_blockers": ["Complex topics", "Hands-on practice time", "Exam scheduling"], "recommended_approach": "Follow structured study plan, practice with labs, take practice exams", "suggested_resources": ["AWS documentation", "Online courses", "Practice exams"]}	2026-01-10 09:00:00	2026-02-08 16:10:57.417287	\N
45cad6cb-f4e2-4360-acab-6f225a5b909b	801690ca-ff26-40f4-aedf-9df316dd19ea	Prepare for Tech Conference	Prepare for upcoming tech conference: research speakers, update LinkedIn profile, prepare elevator pitch, print business cards, plan networking goals, and schedule meetings.	Career	["networking", "conference", "professional", "connections"]	2	7	2	5	pending	20	2026-03-05 23:59:59	\N	{"complexity_score": 2, "estimated_completion_time": 6.0, "potential_blockers": ["Social anxiety", "Time constraints", "Goal clarity"], "recommended_approach": "Set specific networking goals, research attendees, practice conversations", "suggested_resources": ["Conference app", "LinkedIn", "Conversation starters"]}	2026-02-06 16:10:57.420686	2026-02-08 16:10:57.420686	\N
3fd42eea-c747-4af3-95d4-b49e1ab77468	801690ca-ff26-40f4-aedf-9df316dd19ea	365-Day Photography Challenge	Take and edit one photo every day for a year. Focus on different themes each month: portrait, landscape, street, macro, black & white. Currently on day 45.	Hobby	["photography", "creative", "challenge", "art"]	3	6	3	365	in-progress	12	2026-12-31 23:59:59	\N	{"complexity_score": 3, "estimated_completion_time": 400.0, "potential_blockers": ["Consistency", "Creative blocks", "Equipment issues"], "recommended_approach": "Set daily reminder, plan weekly themes, join photo community", "suggested_resources": ["Photo editing software", "Photography tutorials", "Online photo sharing"]}	2026-01-01 08:00:00	2026-02-08 16:11:23.324746	\N
d7852d72-3e24-4a3a-89ba-ce535a132dcc	801690ca-ff26-40f4-aedf-9df316dd19ea	Organize Family Reunion	Plan family reunion for 25+ people. Coordinate venue, catering, activities, accommodations, invitations, and budget. Need to consider various age groups and preferences.	Social	["family", "event", "planning", "reunion"]	2	8	4	20	pending	15	2026-07-15 23:59:59	\N	{"complexity_score": 4, "estimated_completion_time": 25.0, "potential_blockers": ["Scheduling conflicts", "Budget limitations", "Venue availability"], "recommended_approach": "Create planning committee, use online tools for coordination, book early", "suggested_resources": ["Event planning apps", "Venue websites", "Catering services"]}	2026-02-08 16:11:32.636262	2026-02-08 16:11:32.636262	\N
3e6e56dd-c086-420c-9604-f1fc59147859	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	dfgh	sdfg	Work	["d"]	3	5	3	1	pending	0	2026-02-18 03:00:00	\N	{"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}	2026-02-09 22:43:24.760044	2026-02-09 22:43:24.760049	\N
9e5f031d-89f3-4715-84c5-b46b82976156	42d4a5e9-0f84-4bdb-b18e-066166d3aa27	dfgh	sdfg	Work	["sdf"]	3	5	3	1	pending	0	2026-02-17 03:00:00	\N	{"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}	2026-02-09 22:44:26.903586	2026-02-09 22:44:26.903588	\N
26d6df87-0a83-455e-9608-14af94ea551b	801690ca-ff26-40f4-aedf-9df316dd19ea	qwerty	1234567	Other	["qwerty"]	4	8	4	4	in-progress	0	2026-03-03 03:00:00	\N	{"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}	2026-02-17 17:16:03.334181	2026-02-17 17:16:03.334191	\N
36a96a51-b06e-4111-9884-a98a4ad30d08	801690ca-ff26-40f4-aedf-9df316dd19ea	Plan Summer Europe Trip	Plan 2-week trip to Europe visiting Paris, Rome, and Barcelona. Research flights, accommodations, activities, transportation between cities, and create daily itinerary.	Travel	["vacation", "travel", "europe", "planning"]	2	8	3	10	in-progress	60	2026-05-01 03:00:00	\N	{"estimated_completion_time": 4.0, "suggested_resources": [], "complexity_score": 3, "recommended_approach": "Standard approach", "confidence_score": 0.5, "potential_blockers": [], "similar_tasks_completed": 0}	2026-01-29 16:11:13.130219	2026-02-17 14:17:03.559882	\N
\.


--
-- Data for Name: user_preferences; Type: TABLE DATA; Schema: public; Owner: decisionai_user
--

COPY public.user_preferences (id, user_id, theme, notifications, ai_settings, display_settings) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: decisionai_user
--

COPY public.users (id, email, username, password_hash, name, is_active, is_verified, role, preferences, stats, created_at, updated_at, last_login) FROM stdin;
57c5dee8-d936-42ac-9c7e-fdd3d65be816	test4@example.com	\N	$2b$12$BoRJsdKxZG2Y66wG.D6REeVF20dtknoORqpIy5qJUyaIZcx33wxLS	Test User	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-08 07:58:00.524774	2026-02-08 07:58:00.524784	\N
801690ca-ff26-40f4-aedf-9df316dd19ea	test2@example.com	testuser	$2b$12$AzJgg9ZYhGBqqlin0teMceHmXE5Ao9zTjm2EaNTR//.k.IHh/E8Pi	Test User	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-07 16:13:02.532511	2026-02-17 14:12:15.228332	2026-02-17 14:12:15.226404
8d925657-7cb0-4660-a44d-b550fe655a07	samuel4@example.com	samuel	$2b$12$YVAR0g9WBqK/zWI5Hj2i3u7FnqvLhbe7GJnreZHmrSFZa0IN354LC	Samuel admin1	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-07 20:50:10.62844	2026-02-07 20:50:11.329952	2026-02-07 20:50:11.326443
721eeb55-aeb8-43cc-bc1e-eef90a2322b0	test3@example.com	testuser3	$2b$12$xil6cX9mHpGGcBSDWFOhA.38/2BtteX4du.wfc04D33i6hE6u5Zs6	Test User	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-08 07:50:44.63568	2026-02-08 07:50:44.635686	\N
42d4a5e9-0f84-4bdb-b18e-066166d3aa27	samuel.wainaina1@student.moringaschool.com	samuel1	$2b$12$6pHYtAtqWzZX2SEhYwjm1uEXHGKGT/SwfLvhjJFStV0B50bhlldKm	Samuel wainaina	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-08 07:53:32.924475	2026-02-09 19:35:12.826271	2026-02-09 19:35:12.824338
29f31091-6c95-47f7-9d75-556d897cede0	test@example.com	\N	$2b$12$GGbWVygrDLOR.K0.FLY8Zuu0z65i6ThRSvLCboUSjPTMhmHFHBLMO	Test	t	f	user	{"theme": "light", "notifications": true, "ai_enabled": true}	{"total_tasks": 0, "completed_tasks": 0, "avg_completion_time": 0, "productivity_score": 0}	2026-02-07 16:10:40.70475	2026-02-08 11:17:28.499575	2026-02-08 11:17:28.498066
\.


--
-- Name: task_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: decisionai_user
--

SELECT pg_catalog.setval('public.task_history_id_seq', 10, true);


--
-- Name: user_preferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: decisionai_user
--

SELECT pg_catalog.setval('public.user_preferences_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: task_history task_history_pkey; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.task_history
    ADD CONSTRAINT task_history_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_user_id_key; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_key UNIQUE (user_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_user_category; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE INDEX idx_user_category ON public.tasks USING btree (user_id, category);


--
-- Name: idx_user_due_date; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE INDEX idx_user_due_date ON public.tasks USING btree (user_id, due_date);


--
-- Name: idx_user_priority; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE INDEX idx_user_priority ON public.tasks USING btree (user_id, priority);


--
-- Name: idx_user_status; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE INDEX idx_user_status ON public.tasks USING btree (user_id, status);


--
-- Name: ix_tasks_user_id; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE INDEX ix_tasks_user_id ON public.tasks USING btree (user_id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: decisionai_user
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: task_history task_history_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.task_history
    ADD CONSTRAINT task_history_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: task_history task_history_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.task_history
    ADD CONSTRAINT task_history_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: tasks tasks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: decisionai_user
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict JDUKtL4hfoh3XNrbgguV5CqpwmKipHGqXuQVLvXnbpqLJRoVGP80cBAJ7eT2VeX

