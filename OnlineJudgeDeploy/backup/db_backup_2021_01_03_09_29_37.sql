--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Drop databases
--

DROP DATABASE onlinejudge;




--
-- Drop roles
--

DROP ROLE onlinejudge;


--
-- Roles
--

CREATE ROLE onlinejudge;
ALTER ROLE onlinejudge WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS PASSWORD 'md54827417b344ff91a2f608bbad9b4e488';






--
-- Database creation
--

CREATE DATABASE onlinejudge WITH TEMPLATE = template0 OWNER = onlinejudge;
REVOKE CONNECT,TEMPORARY ON DATABASE template1 FROM PUBLIC;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect onlinejudge

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15
-- Dumped by pg_dump version 10.15

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: acm_contest_rank; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.acm_contest_rank (
    id integer NOT NULL,
    submission_number integer NOT NULL,
    accepted_number integer NOT NULL,
    total_time integer NOT NULL,
    submission_info jsonb NOT NULL,
    contest_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.acm_contest_rank OWNER TO onlinejudge;

--
-- Name: acm_contest_rank_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.acm_contest_rank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.acm_contest_rank_id_seq OWNER TO onlinejudge;

--
-- Name: acm_contest_rank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.acm_contest_rank_id_seq OWNED BY public.acm_contest_rank.id;


--
-- Name: announcement; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.announcement (
    id integer NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    create_time timestamp with time zone NOT NULL,
    last_update_time timestamp with time zone NOT NULL,
    visible boolean NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE public.announcement OWNER TO onlinejudge;

--
-- Name: announcement_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.announcement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.announcement_id_seq OWNER TO onlinejudge;

--
-- Name: announcement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.announcement_id_seq OWNED BY public.announcement.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO onlinejudge;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO onlinejudge;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO onlinejudge;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO onlinejudge;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO onlinejudge;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO onlinejudge;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: contest; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.contest (
    id integer NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    real_time_rank boolean NOT NULL,
    password text,
    rule_type text NOT NULL,
    start_time timestamp with time zone NOT NULL,
    end_time timestamp with time zone NOT NULL,
    create_time timestamp with time zone NOT NULL,
    last_update_time timestamp with time zone NOT NULL,
    visible boolean NOT NULL,
    created_by_id integer NOT NULL,
    allowed_ip_ranges jsonb NOT NULL
);


ALTER TABLE public.contest OWNER TO onlinejudge;

--
-- Name: contest_announcement; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.contest_announcement (
    id integer NOT NULL,
    title text NOT NULL,
    content text NOT NULL,
    create_time timestamp with time zone NOT NULL,
    contest_id integer NOT NULL,
    created_by_id integer NOT NULL,
    visible boolean NOT NULL
);


ALTER TABLE public.contest_announcement OWNER TO onlinejudge;

--
-- Name: contest_announcement_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.contest_announcement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contest_announcement_id_seq OWNER TO onlinejudge;

--
-- Name: contest_announcement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.contest_announcement_id_seq OWNED BY public.contest_announcement.id;


--
-- Name: contest_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.contest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contest_id_seq OWNER TO onlinejudge;

--
-- Name: contest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.contest_id_seq OWNED BY public.contest.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO onlinejudge;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO onlinejudge;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_dramatiq_task; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.django_dramatiq_task (
    id uuid NOT NULL,
    status character varying(8) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    message_data bytea NOT NULL
);


ALTER TABLE public.django_dramatiq_task OWNER TO onlinejudge;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO onlinejudge;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO onlinejudge;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO onlinejudge;

--
-- Name: judge_server; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.judge_server (
    id integer NOT NULL,
    hostname text NOT NULL,
    ip text,
    judger_version text NOT NULL,
    cpu_core integer NOT NULL,
    memory_usage double precision NOT NULL,
    cpu_usage double precision NOT NULL,
    last_heartbeat timestamp with time zone NOT NULL,
    create_time timestamp with time zone NOT NULL,
    task_number integer NOT NULL,
    service_url text,
    is_disabled boolean NOT NULL
);


ALTER TABLE public.judge_server OWNER TO onlinejudge;

--
-- Name: judge_server_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.judge_server_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.judge_server_id_seq OWNER TO onlinejudge;

--
-- Name: judge_server_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.judge_server_id_seq OWNED BY public.judge_server.id;


--
-- Name: oi_contest_rank; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.oi_contest_rank (
    id integer NOT NULL,
    submission_number integer NOT NULL,
    total_score integer NOT NULL,
    submission_info jsonb NOT NULL,
    contest_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.oi_contest_rank OWNER TO onlinejudge;

--
-- Name: oi_contest_rank_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.oi_contest_rank_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.oi_contest_rank_id_seq OWNER TO onlinejudge;

--
-- Name: oi_contest_rank_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.oi_contest_rank_id_seq OWNED BY public.oi_contest_rank.id;


--
-- Name: options_sysoptions; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.options_sysoptions (
    id integer NOT NULL,
    key text NOT NULL,
    value jsonb NOT NULL
);


ALTER TABLE public.options_sysoptions OWNER TO onlinejudge;

--
-- Name: options_sysoptions_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.options_sysoptions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.options_sysoptions_id_seq OWNER TO onlinejudge;

--
-- Name: options_sysoptions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.options_sysoptions_id_seq OWNED BY public.options_sysoptions.id;


--
-- Name: problem; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.problem (
    id integer NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    input_description text NOT NULL,
    output_description text NOT NULL,
    samples jsonb NOT NULL,
    test_case_id text NOT NULL,
    test_case_score jsonb NOT NULL,
    hint text,
    languages jsonb NOT NULL,
    template jsonb NOT NULL,
    create_time timestamp with time zone NOT NULL,
    last_update_time timestamp with time zone,
    time_limit integer NOT NULL,
    memory_limit integer NOT NULL,
    spj boolean NOT NULL,
    spj_language text,
    spj_code text,
    spj_version text,
    rule_type text NOT NULL,
    visible boolean NOT NULL,
    difficulty text NOT NULL,
    source text,
    submission_number bigint NOT NULL,
    accepted_number bigint NOT NULL,
    created_by_id integer NOT NULL,
    _id text NOT NULL,
    statistic_info jsonb NOT NULL,
    total_score integer NOT NULL,
    contest_id integer,
    is_public boolean NOT NULL,
    spj_compile_ok boolean NOT NULL,
    io_mode jsonb NOT NULL,
    share_submission boolean NOT NULL
);


ALTER TABLE public.problem OWNER TO onlinejudge;

--
-- Name: problem_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.problem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problem_id_seq OWNER TO onlinejudge;

--
-- Name: problem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.problem_id_seq OWNED BY public.problem.id;


--
-- Name: problem_tag; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.problem_tag (
    id integer NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.problem_tag OWNER TO onlinejudge;

--
-- Name: problem_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.problem_tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problem_tag_id_seq OWNER TO onlinejudge;

--
-- Name: problem_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.problem_tag_id_seq OWNED BY public.problem_tag.id;


--
-- Name: problem_tags; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.problem_tags (
    id integer NOT NULL,
    problem_id integer NOT NULL,
    problemtag_id integer NOT NULL
);


ALTER TABLE public.problem_tags OWNER TO onlinejudge;

--
-- Name: problem_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.problem_tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.problem_tags_id_seq OWNER TO onlinejudge;

--
-- Name: problem_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.problem_tags_id_seq OWNED BY public.problem_tags.id;


--
-- Name: submission; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.submission (
    id text NOT NULL,
    contest_id integer,
    problem_id integer NOT NULL,
    create_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    code text NOT NULL,
    result integer NOT NULL,
    info jsonb NOT NULL,
    language text NOT NULL,
    shared boolean NOT NULL,
    statistic_info jsonb NOT NULL,
    username text NOT NULL,
    ip text
);


ALTER TABLE public.submission OWNER TO onlinejudge;

--
-- Name: user; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    username text NOT NULL,
    email text,
    create_time timestamp with time zone,
    admin_type text NOT NULL,
    reset_password_token text,
    reset_password_token_expire_time timestamp with time zone,
    auth_token text,
    two_factor_auth boolean NOT NULL,
    tfa_token text,
    open_api boolean NOT NULL,
    open_api_appkey text,
    is_disabled boolean NOT NULL,
    problem_permission text NOT NULL,
    session_keys jsonb NOT NULL
);


ALTER TABLE public."user" OWNER TO onlinejudge;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO onlinejudge;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: user_profile; Type: TABLE; Schema: public; Owner: onlinejudge
--

CREATE TABLE public.user_profile (
    id integer NOT NULL,
    acm_problems_status jsonb NOT NULL,
    avatar text NOT NULL,
    blog character varying(200),
    mood text,
    accepted_number integer NOT NULL,
    submission_number integer NOT NULL,
    github text,
    school text,
    major text,
    user_id integer NOT NULL,
    total_score bigint NOT NULL,
    oi_problems_status jsonb NOT NULL,
    real_name text,
    language text
);


ALTER TABLE public.user_profile OWNER TO onlinejudge;

--
-- Name: user_profile_id_seq; Type: SEQUENCE; Schema: public; Owner: onlinejudge
--

CREATE SEQUENCE public.user_profile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_profile_id_seq OWNER TO onlinejudge;

--
-- Name: user_profile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: onlinejudge
--

ALTER SEQUENCE public.user_profile_id_seq OWNED BY public.user_profile.id;


--
-- Name: acm_contest_rank id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.acm_contest_rank ALTER COLUMN id SET DEFAULT nextval('public.acm_contest_rank_id_seq'::regclass);


--
-- Name: announcement id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.announcement ALTER COLUMN id SET DEFAULT nextval('public.announcement_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: contest id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest ALTER COLUMN id SET DEFAULT nextval('public.contest_id_seq'::regclass);


--
-- Name: contest_announcement id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest_announcement ALTER COLUMN id SET DEFAULT nextval('public.contest_announcement_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: judge_server id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.judge_server ALTER COLUMN id SET DEFAULT nextval('public.judge_server_id_seq'::regclass);


--
-- Name: oi_contest_rank id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.oi_contest_rank ALTER COLUMN id SET DEFAULT nextval('public.oi_contest_rank_id_seq'::regclass);


--
-- Name: options_sysoptions id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.options_sysoptions ALTER COLUMN id SET DEFAULT nextval('public.options_sysoptions_id_seq'::regclass);


--
-- Name: problem id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem ALTER COLUMN id SET DEFAULT nextval('public.problem_id_seq'::regclass);


--
-- Name: problem_tag id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tag ALTER COLUMN id SET DEFAULT nextval('public.problem_tag_id_seq'::regclass);


--
-- Name: problem_tags id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tags ALTER COLUMN id SET DEFAULT nextval('public.problem_tags_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_profile id; Type: DEFAULT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.user_profile ALTER COLUMN id SET DEFAULT nextval('public.user_profile_id_seq'::regclass);


--
-- Data for Name: acm_contest_rank; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.acm_contest_rank (id, submission_number, accepted_number, total_time, submission_info, contest_id, user_id) FROM stdin;
\.


--
-- Data for Name: announcement; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.announcement (id, title, content, create_time, last_update_time, visible, created_by_id) FROM stdin;
3	[SKKU Coding Platform 모의대회]	<p>일시 : 1/4(월) - 1/10(일)</p><p>참여 방법 : 상단의 &#039;SKKU Coding Platform 모의대회&#039; 클릭 후 참여</p><p>참여 혜택 : 스타벅스 5000원 상품권 증정</p><p>참여 조건 : 한 문제 이상 풀기</p>	2020-12-31 06:05:15.232671+00	2020-12-31 06:05:15.232713+00	t	1
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add session	3	add_session
10	Can change session	3	change_session
11	Can delete session	3	delete_session
12	Can view session	3	view_session
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add task	5	add_task
18	Can change task	5	change_task
19	Can delete task	5	delete_task
20	Can view task	5	view_task
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add user profile	7	add_userprofile
26	Can change user profile	7	change_userprofile
27	Can delete user profile	7	delete_userprofile
28	Can view user profile	7	view_userprofile
29	Can add announcement	8	add_announcement
30	Can change announcement	8	change_announcement
31	Can delete announcement	8	delete_announcement
32	Can view announcement	8	view_announcement
33	Can add judge server	9	add_judgeserver
34	Can change judge server	9	change_judgeserver
35	Can delete judge server	9	delete_judgeserver
36	Can view judge server	9	view_judgeserver
37	Can add problem	10	add_problem
38	Can change problem	10	change_problem
39	Can delete problem	10	delete_problem
40	Can view problem	10	view_problem
41	Can add problem tag	11	add_problemtag
42	Can change problem tag	11	change_problemtag
43	Can delete problem tag	11	delete_problemtag
44	Can view problem tag	11	view_problemtag
45	Can add acm contest rank	12	add_acmcontestrank
46	Can change acm contest rank	12	change_acmcontestrank
47	Can delete acm contest rank	12	delete_acmcontestrank
48	Can view acm contest rank	12	view_acmcontestrank
49	Can add contest	13	add_contest
50	Can change contest	13	change_contest
51	Can delete contest	13	delete_contest
52	Can view contest	13	view_contest
53	Can add contest announcement	14	add_contestannouncement
54	Can change contest announcement	14	change_contestannouncement
55	Can delete contest announcement	14	delete_contestannouncement
56	Can view contest announcement	14	view_contestannouncement
57	Can add oi contest rank	15	add_oicontestrank
58	Can change oi contest rank	15	change_oicontestrank
59	Can delete oi contest rank	15	delete_oicontestrank
60	Can view oi contest rank	15	view_oicontestrank
61	Can add submission	16	add_submission
62	Can change submission	16	change_submission
63	Can delete submission	16	delete_submission
64	Can view submission	16	view_submission
65	Can add sys options	17	add_sysoptions
66	Can change sys options	17	change_sysoptions
67	Can delete sys options	17	delete_sysoptions
68	Can view sys options	17	view_sysoptions
\.


--
-- Data for Name: contest; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.contest (id, title, description, real_time_rank, password, rule_type, start_time, end_time, create_time, last_update_time, visible, created_by_id, allowed_ip_ranges) FROM stdin;
1	Test Contest	<p>Test Contest</p>	t	1	ACM	2020-12-23 15:00:00+00	2020-12-24 15:00:00+00	2020-12-23 08:47:09.775124+00	2020-12-23 08:49:15.291024+00	f	1	[]
2	SKKU Coding Platform 모의대회	<p>일시 : 1/4(월) - 1/10(일)</p><p>대회 참여 시 스타벅스 5000원 상품권을 드립니다.</p><p>※ 대회 참여 조건 : 한 문제 이상 풀기</p>	t	\N	ACM	2021-01-03 15:00:00+00	2021-01-10 14:59:59+00	2020-12-31 05:58:59.332909+00	2021-01-02 14:46:48.410537+00	t	1	[]
\.


--
-- Data for Name: contest_announcement; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.contest_announcement (id, title, content, create_time, contest_id, created_by_id, visible) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	sessions	session
4	contenttypes	contenttype
5	django_dramatiq	task
6	account	user
7	account	userprofile
8	announcement	announcement
9	conf	judgeserver
10	problem	problem
11	problem	problemtag
12	contest	acmcontestrank
13	contest	contest
14	contest	contestannouncement
15	contest	oicontestrank
16	submission	submission
17	options	sysoptions
\.


--
-- Data for Name: django_dramatiq_task; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.django_dramatiq_task (id, status, created_at, updated_at, message_data) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	account	0001_initial	2020-12-17 08:13:39.32859+00
2	account	0002_auto_20170209_1028	2020-12-17 08:13:39.356333+00
3	account	0003_userprofile_total_score	2020-12-17 08:13:39.381432+00
4	account	0005_auto_20170830_1154	2020-12-17 08:13:39.412432+00
5	account	0006_user_session_keys	2020-12-17 08:13:39.443787+00
6	account	0008_auto_20171011_1214	2020-12-17 08:13:39.6466+00
7	account	0009_auto_20171125_1514	2020-12-17 08:13:39.652618+00
8	account	0010_auto_20180501_0436	2020-12-17 08:13:39.683892+00
9	account	0011_auto_20180501_0456	2020-12-17 08:13:39.689848+00
10	account	0012_userprofile_language	2020-12-17 08:13:39.695828+00
11	announcement	0001_initial	2020-12-17 08:13:39.715801+00
12	announcement	0002_auto_20171011_1214	2020-12-17 08:13:39.727117+00
13	announcement	0003_auto_20180501_0436	2020-12-17 08:13:39.732273+00
14	contenttypes	0001_initial	2020-12-17 08:13:39.746147+00
15	contenttypes	0002_remove_content_type_name	2020-12-17 08:13:39.756642+00
16	auth	0001_initial	2020-12-17 08:13:39.812592+00
17	auth	0002_alter_permission_name_max_length	2020-12-17 08:13:39.819882+00
18	auth	0003_alter_user_email_max_length	2020-12-17 08:13:39.826622+00
19	auth	0004_alter_user_username_opts	2020-12-17 08:13:39.832436+00
20	auth	0005_alter_user_last_login_null	2020-12-17 08:13:39.836744+00
21	auth	0006_require_contenttypes_0002	2020-12-17 08:13:39.838678+00
22	auth	0007_alter_validators_add_error_messages	2020-12-17 08:13:39.842962+00
23	auth	0008_alter_user_username_max_length	2020-12-17 08:13:39.84867+00
24	auth	0009_alter_user_last_name_max_length	2020-12-17 08:13:39.854517+00
25	conf	0001_initial	2020-12-17 08:13:39.887611+00
26	conf	0002_auto_20171011_1214	2020-12-17 08:13:39.919021+00
27	conf	0003_judgeserver_is_disabled	2020-12-17 08:13:39.930211+00
28	conf	0004_auto_20180501_0436	2020-12-17 08:13:39.945343+00
29	problem	0001_initial	2020-12-17 08:13:39.998182+00
30	contest	0001_initial	2020-12-17 08:13:40.16192+00
31	contest	0002_auto_20170209_0845	2020-12-17 08:13:40.222473+00
32	contest	0003_auto_20170217_0820	2020-12-17 08:13:40.281608+00
33	contest	0004_auto_20170717_1324	2020-12-17 08:13:40.298044+00
34	contest	0005_auto_20170823_0918	2020-12-17 08:13:40.31889+00
35	contest	0006_auto_20171011_1214	2020-12-17 08:13:40.3808+00
36	contest	0007_contestannouncement_visible	2020-12-17 08:13:40.409095+00
37	contest	0008_contest_allowed_ip_ranges	2020-12-17 08:13:40.434856+00
38	contest	0009_auto_20180501_0436	2020-12-17 08:13:40.465583+00
39	contest	0010_auto_20190326_0201	2020-12-17 08:13:40.493896+00
40	django_dramatiq	0001_initial	2020-12-17 08:13:40.50715+00
41	options	0001_initial	2020-12-17 08:13:40.528687+00
42	options	0002_auto_20180501_0436	2020-12-17 08:13:40.535633+00
43	options	0003_migrate_languages_options	2020-12-17 08:13:40.539231+00
44	submission	0001_initial	2020-12-17 08:13:40.568102+00
45	submission	0002_auto_20170509_1203	2020-12-17 08:13:40.582884+00
46	submission	0005_submission_username	2020-12-17 08:13:40.612455+00
47	submission	0006_auto_20170830_1154	2020-12-17 08:13:40.622621+00
48	submission	0007_auto_20170923_1318	2020-12-17 08:13:40.740766+00
49	submission	0008_submission_ip	2020-12-17 08:13:40.749352+00
50	submission	0009_delete_user_output	2020-12-17 08:13:40.765097+00
51	problem	0002_problem__id	2020-12-17 08:13:40.79649+00
52	problem	0003_auto_20170217_0820	2020-12-17 08:13:40.872225+00
53	problem	0004_auto_20170501_0637	2020-12-17 08:13:41.008096+00
54	problem	0005_auto_20170815_1258	2020-12-17 08:13:41.080772+00
55	problem	0006_auto_20170823_0918	2020-12-17 08:13:41.141604+00
56	problem	0008_auto_20170923_1318	2020-12-17 08:13:41.31804+00
57	problem	0009_auto_20171011_1214	2020-12-17 08:13:41.538471+00
58	problem	0010_problem_spj_compile_ok	2020-12-17 08:13:41.575946+00
59	problem	0011_fix_problem_ac_count	2020-12-17 08:13:41.594763+00
60	problem	0012_auto_20180501_0436	2020-12-17 08:13:41.687031+00
61	problem	0013_problem_io_mode	2020-12-17 08:13:41.72484+00
62	problem	0014_problem_share_submission	2020-12-17 08:13:41.75849+00
63	sessions	0001_initial	2020-12-17 08:13:41.779732+00
64	submission	0011_fix_submission_number	2020-12-17 08:13:41.798576+00
65	submission	0012_auto_20180501_0436	2020-12-17 08:13:41.824871+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: judge_server; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.judge_server (id, hostname, ip, judger_version, cpu_core, memory_usage, cpu_usage, last_heartbeat, create_time, task_number, service_url, is_disabled) FROM stdin;
2	c5077d7ca3b3	172.18.0.4	2.1.1	64	8	25	2021-01-03 00:29:34.822894+00	2020-12-27 05:13:15.945009+00	0	http://judge-server:8080	f
\.


--
-- Data for Name: oi_contest_rank; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.oi_contest_rank (id, submission_number, total_score, submission_info, contest_id, user_id) FROM stdin;
\.


--
-- Data for Name: options_sysoptions; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.options_sysoptions (id, key, value) FROM stdin;
7	smtp_config	{}
9	throttling	{"ip": {"capacity": 100, "fill_rate": 0.1, "default_capacity": 50}, "user": {"capacity": 20, "fill_rate": 0.03, "default_capacity": 10}}
10	languages	[{"spj": {"config": {"command": "{exe_path} {in_file_path} {user_out_file_path}", "exe_name": "spj-{spj_version}", "seccomp_rule": "c_cpp"}, "compile": {"exe_name": "spj-{spj_version}", "src_name": "spj-{spj_version}.c", "max_memory": 1073741824, "max_cpu_time": 3000, "max_real_time": 10000, "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c11 {src_path} -lm -o {exe_path}"}}, "name": "C", "config": {"run": {"env": ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"], "command": "{exe_path}", "seccomp_rule": {"File IO": "c_cpp_file_io", "Standard IO": "c_cpp"}}, "compile": {"exe_name": "main", "src_name": "main.c", "max_memory": 268435456, "max_cpu_time": 3000, "max_real_time": 10000, "compile_command": "/usr/bin/gcc -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c11 {src_path} -lm -o {exe_path}"}, "template": "//PREPEND BEGIN\\n#include <stdio.h>\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\nint add(int a, int b) {\\n  // Please fill this blank\\n  return ___________;\\n}\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\nint main() {\\n  printf(\\"%d\\", add(1, 2));\\n  return 0;\\n}\\n//APPEND END"}, "description": "GCC 5.4", "content_type": "text/x-csrc"}, {"spj": {"config": {"command": "{exe_path} {in_file_path} {user_out_file_path}", "exe_name": "spj-{spj_version}", "seccomp_rule": "c_cpp"}, "compile": {"exe_name": "spj-{spj_version}", "src_name": "spj-{spj_version}.cpp", "max_memory": 1073741824, "max_cpu_time": 10000, "max_real_time": 20000, "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++14 {src_path} -lm -o {exe_path}"}}, "name": "C++", "config": {"run": {"env": ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"], "command": "{exe_path}", "seccomp_rule": {"File IO": "c_cpp_file_io", "Standard IO": "c_cpp"}}, "compile": {"exe_name": "main", "src_name": "main.cpp", "max_memory": 1073741824, "max_cpu_time": 10000, "max_real_time": 20000, "compile_command": "/usr/bin/g++ -DONLINE_JUDGE -O2 -w -fmax-errors=3 -std=c++14 {src_path} -lm -o {exe_path}"}, "template": "//PREPEND BEGIN\\n#include <iostream>\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\nint add(int a, int b) {\\n  // Please fill this blank\\n  return ___________;\\n}\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\nint main() {\\n  std::cout << add(1, 2);\\n  return 0;\\n}\\n//APPEND END"}, "description": "G++ 5.4", "content_type": "text/x-c++src"}, {"name": "Java", "config": {"run": {"env": ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"], "command": "/usr/bin/java -cp {exe_dir} -XX:MaxRAM={max_memory}k -Djava.security.manager -Dfile.encoding=UTF-8 -Djava.security.policy==/etc/java_policy -Djava.awt.headless=true Main", "seccomp_rule": null, "memory_limit_check_only": 1}, "compile": {"exe_name": "Main", "src_name": "Main.java", "max_memory": -1, "max_cpu_time": 5000, "max_real_time": 10000, "compile_command": "/usr/bin/javac {src_path} -d {exe_dir} -encoding UTF8"}, "template": "//PREPEND BEGIN\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\n//APPEND END"}, "description": "OpenJDK 1.8", "content_type": "text/x-java"}, {"name": "Python2", "config": {"run": {"env": ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"], "command": "/usr/bin/python {exe_path}", "seccomp_rule": "general"}, "compile": {"exe_name": "solution.pyc", "src_name": "solution.py", "max_memory": 134217728, "max_cpu_time": 3000, "max_real_time": 10000, "compile_command": "/usr/bin/python -m py_compile {src_path}"}, "template": "//PREPEND BEGIN\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\n//APPEND END"}, "description": "Python 2.7", "content_type": "text/x-python"}, {"name": "Python3", "config": {"run": {"env": ["LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8", "PYTHONIOENCODING=utf-8"], "command": "/usr/bin/python3 {exe_path}", "seccomp_rule": "general"}, "compile": {"exe_name": "__pycache__/solution.cpython-36.pyc", "src_name": "solution.py", "max_memory": 134217728, "max_cpu_time": 3000, "max_real_time": 10000, "compile_command": "/usr/bin/python3 -m py_compile {src_path}"}, "template": "//PREPEND BEGIN\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\n//APPEND END"}, "description": "Python 3.6", "content_type": "text/x-python"}, {"name": "Golang", "config": {"run": {"env": ["GODEBUG=madvdontneed=1", "LANG=en_US.UTF-8", "LANGUAGE=en_US:en", "LC_ALL=en_US.UTF-8"], "command": "{exe_path}", "seccomp_rule": "", "memory_limit_check_only": 1}, "compile": {"env": ["GOCACHE=/tmp"], "exe_name": "main", "src_name": "main.go", "max_memory": 1073741824, "max_cpu_time": 3000, "max_real_time": 5000, "compile_command": "/usr/bin/go build -o {exe_path} {src_path}"}, "template": "//PREPEND BEGIN\\n//PREPEND END\\n\\n//TEMPLATE BEGIN\\n//TEMPLATE END\\n\\n//APPEND BEGIN\\n//APPEND END"}, "description": "Golang 1.14", "content_type": "text/x-go"}]
1	website_base_url	"http://127.0.0.1"
2	website_name	"SKKU"
3	website_name_shortcut	"SKKU Coding Platform"
4	website_footer	"SKKU Coding Platform"
5	allow_register	true
6	submission_list_show_all	true
8	judge_server_token	"CHANGE_THIS"
\.


--
-- Data for Name: problem; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.problem (id, title, description, input_description, output_description, samples, test_case_id, test_case_score, hint, languages, template, create_time, last_update_time, time_limit, memory_limit, spj, spj_language, spj_code, spj_version, rule_type, visible, difficulty, source, submission_number, accepted_number, created_by_id, _id, statistic_info, total_score, contest_id, is_public, spj_compile_ok, io_mode, share_submission) FROM stdin;
6	문제 출력 테스트	<p>나무위키는2015년4월 17일(KST)에 만들어진,서브컬쳐에 특화된위키사이트이다. 본사는파라과이아순시온에 위치해 있다.</p><p>로고 및 패비콘, 마스코트(캐릭터), 슬로건은 유저들의 자발적 임시 공모로 시작해 운영진의 공식 결정으로 각 항목이 결정되었다. 각 항목에 관한 문서는나무위키:보존문서/비공식 로고,나무위키:보존문서/비공식 캐릭터,나무위키:보존문서/비공식 패비콘,나무위키:보존문서/비공식 슬로건을 참고하길 바란다. 많은 위키러들이 참여해서 로고는 103개, 캐릭터는 51개, 슬로건은 무려 145개의 시안으로 모집이 마감되었다. 현재는시안 32가선정된 상태다.[7]패비콘은로고와 같은 시안 5가 선정되었으며마스코트(캐릭터)는세피로트와무냐가 선정되었다. 그러나 선출 과정에서 문제가 있다는 논란과 함께 나무위키의 상징이라고 하기에는 약간 아쉽다는 의견도 있다. 그리고 일반인 사용자들이 많아졌음에도교복이나트윈테일등 비교적 덕후 계층 사용자들에게 선호될만한 모습을 보여서 비덕후 사용자 사이에선 호불호가 갈린다. 차라리옆동네처럼 비인간형이라면 그나마 더 낫겠지만...</p><p>슬로건은 투표에서 1위를 한시안 109&quot;나무위키, 여러분이 가꾸어 나가는 지식의 나무.&quot;[8]가 선정되었다.#</p><p>개설자들의 신상은 비공개고, 아이디는namu,PPPP,kasio이다.ztirf,syndrome은 초창기 운영진이지만 설립 멤버는 아니라고 하여namu 본인이 수정하였다.</p><p>namu - 백엔드 개발자</p><p>PPPP - 프론트엔드 개발자</p><p>kasio - 렌더러 개발자</p><p>ztirf - 위키 관리 및 게시판 관리</p><p>syndrome - 이슈 트래커 및 기타 이슈 관리.</p><p>운영진 역할에 대한 정리는 여기를 참고하자</p><p>개설자는리그베다 위키 게시판에유동닉으로 처음 등장했으며, 2015년 4월 내내 아직 정확한 신원을 밝히지 않고 있다. 나무위키 개설자들은 특정 단체나 집단의 이익을 위해 행동하고 있지 않으며, 나무위키 개설자들은 지식의 사유화를 반대하며 평화로운 방식으로 지식의 자유로운 공유를 지원하는 것이 목표라고 한다.2015년 4월 26일 자정 무렵, syndrome이라는 아이디로&quot;(공식) 이때까지 나온 나무위키에 대한 질문에 대한 답변입니다.&quot;라는 글이 올라왔다. 이후 해당 글이 위키 게시판으로 이전된 상태다.개설자들이 신원을 밝히지 않는 이유는 법적 분쟁을 의식해서다. 일단 신원이 밝혀지는 순간 해당 위키의 문서들에 불만이 있는 개인 혹은 단체들이 사방에서 고소를 걸 가능성이 100% 인데다[9]리그베다 위키 측에서 법무법인을 동원한 광범위한 고소를 할 가능성도 배제할 수 없으므로 익명을 유지하고 있다. 일단 관리자의답변에 따르면보안관련 일을 하고 있다고 한다.</p><p>나무위키가umanle S.R.L.이라는 단체에 인수된 이후 위의 개설자들은 어떠한 권한도 가지고 있지 않다. 2016년 4.13 총선이 끝나고 나무위키가파라과이법인에 넘어가고 namu를 거꾸로 쓴 uman을 이름으로 사용하자, 국정원 댓글 요원 김하영이 &#039;논지&#039; 파일을 &#039;지논&#039;으로 거꾸로 써서 들고 다닌 것을 떠올리며국정원특유의 교란 네이밍 방식이라고 추정하는 이들도 있었다,</p>	<p><span style="color: rgb(51, 51, 51);">개설자는리그베다 위키 게시판에유동닉으로 처음 등장했으며, 2015년 4월 내내 아직 정확한 신원을 밝히지 않고 있다. 나무위키 개설자들은 특정 단체나 집단의 이익을 위해 행동하고 있지 않으며, 나무위키 개설자들은 지식의 사유화를 반대하며 평화로운 방식으로 지식의 자유로운 공유를 지원하는 것이 목표라고 한다.</span><span style="color: rgb(51, 51, 51);">2015년 4월 26일 자정 무렵, syndrome이라는 아이디로&quot;(공식) 이때까지 나온 나무위키에 대한 질문에 대한 답변입니다.&quot;라는 글이 올라왔다. 이후 해당 글이 위키 게시판으로 이전된 상태다.</span><span style="color: rgb(51, 51, 51);">개설자들이 신원을 밝히지 않는 이유는 법적 분쟁을 의식해서다. 일단 신원이 밝혀지는 순간 해당 위키의 문서들에 불만이 있는 개인 혹은 단체들이 사방에서 고소를 걸 가능성이 100% 인데다[9]리그베다 위키 측에서 법무법인을 동원한 광범위한 고소를 할 가능성도 배제할 수 없으므로 익명을 유지하고 있다. 일단 관리자의답변에 따르면보안관련 일을 하고 있다고 한다.</span><br /></p>	<p><span style="color: rgb(51, 51, 51);">개설자는리그베다 위키 게시판에유동닉으로 처음 등장했으며, 2015년 4월 내내 아직 정확한 신원을 밝히지 않고 있다. 나무위키 개설자들은 특정 단체나 집단의 이익을 위해 행동하고 있지 않으며, 나무위키 개설자들은 지식의 사유화를 반대하며 평화로운 방식으로 지식의 자유로운 공유를 지원하는 것이 목표라고 한다.</span><span style="color: rgb(51, 51, 51);">2015년 4월 26일 자정 무렵, syndrome이라는 아이디로&quot;(공식) 이때까지 나온 나무위키에 대한 질문에 대한 답변입니다.&quot;라는 글이 올라왔다. 이후 해당 글이 위키 게시판으로 이전된 상태다.</span><span style="color: rgb(51, 51, 51);">개설자들이 신원을 밝히지 않는 이유는 법적 분쟁을 의식해서다. 일단 신원이 밝혀지는 순간 해당 위키의 문서들에 불만이 있는 개인 혹은 단체들이 사방에서 고소를 걸 가능성이 100% 인데다[9]리그베다 위키 측에서 법무법인을 동원한 광범위한 고소를 할 가능성도 배제할 수 없으므로 익명을 유지하고 있다. 일단 관리자의답변에 따르면보안관련 일을 하고 있다고 한다.</span><br /></p>	[{"input": "N", "output": "G"}]	6d4ae49d258f2cd61088d9f30e4a8112	[{"score": 50, "input_name": "1.in", "output_name": "1.out"}, {"score": 50, "input_name": "2.in", "output_name": "2.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2020-12-31 11:43:55.197949+00	\N	1000	256	f	\N	\N	\N	ACM	f	Low		0	0	1	Z	{}	0	\N	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
10	가파른 경사	<p>처음으로 인사캠을 방문한 율전이는 너무나 가파른 오르막길에 놀랐다.이를본 율전이는 인사캠의 경사가 얼마나 심한지 알기 위해 네 지점의 높이를 측정하기로 마음먹었다.이때율전이는 측정한 높이를 다음과 같이 네 가지 경우로 나누려고 한다. (단,측정한 순서는 유지한다)</p><p style="margin-left: 38pt;">1.4개의 강한 단조증가(strictly increasing)하는 높이를 읽은 경우(“Uphill”)(예: 3 4 7 9)</p><p style="margin-left: 38pt;">2.4개의 강한 단조감소(strictly decreasing)하는 높이를 읽은 경우(“Downhill”)(예: 9 6 5 2)</p><p style="margin-left: 38pt;">3.4개의 일정한 높이를 읽은 경우(“Flat Land”) (예: 5 5 5 5)</p><p style="margin-left: 38pt;">4.위 경우 중 어느 것에도 속하지 않는 경우(“Unknown”)</p><p>율전이가 측정한 높이가 주어졌을 때,어떤 경우에 속하는지 출력하라.</p>	<p>네 줄에 걸쳐 높이 $h_i$가 주어진다.(0 &lt; $h_i \\le$ 100)<br /></p>	<p>만약 네 개의 높이가 강한 단조증가(strictly increasing)면“Uphill”,강한 단조감소(strictly decreasing)면“Downhill”을 출력한다.또한 높이가 일정하다면“Flat Land”를 출력하고,어느 경우에도 속하지 않으면“Unknown”을 출력한다.<br /></p>	[{"input": "1\\n10\\n12\\n13\\n", "output": "Uphill"}]	9130c1c1db738bb7d9d9c6580ccf2933	[{"score": 20, "input_name": "1.in", "output_name": "1.out"}, {"score": 20, "input_name": "2.in", "output_name": "2.out"}, {"score": 20, "input_name": "3.in", "output_name": "3.out"}, {"score": 20, "input_name": "4.in", "output_name": "4.out"}, {"score": 20, "input_name": "5.in", "output_name": "5.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 07:14:47.225125+00	\N	1000	256	f	\N	\N	\N	ACM	f	Low		0	0	1	A	{}	0	\N	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
12	가파른 경사	<p>처음으로 인사캠을 방문한 율전이는 너무나 가파른 오르막길에 놀랐다. 이를 본 율전이는 인사캠의 경사가 얼마나 심한지 알기 위해 네 지점의 높이를 측정하기로 마음먹었다.이때 율전이는 측정한 높이를 다음과 같이 네 가지 경우로 나누려고 한다. (단,측정한 순서는 유지한다)</p><p style="margin-left: 38pt;">1.4개의 강한 단조증가(strictly increasing)하는 높이를 읽은 경우(“Uphill”)(예: 3 4 7 9)</p><p style="margin-left: 38pt;">2.4개의 강한 단조감소(strictly decreasing)하는 높이를 읽은 경우(“Downhill”)(예: 9 6 5 2)</p><p style="margin-left: 38pt;">3.4개의 일정한 높이를 읽은 경우(“Flat Land”) (예: 5 5 5 5)</p><p style="margin-left: 38pt;">4.위 경우 중 어느 것에도 속하지 않는 경우(“Unknown”)</p><p>율전이가 측정한 높이가 주어졌을 때,어떤 경우에 속하는지 출력하라.</p>	<p>네 줄에 걸쳐 높이 $h_i$가 주어진다. (0 $\\lt h_i \\le$ 100)<br /></p>	<p>만약 네 개의 높이가 강한 단조증가(strictly increasing)면 “Uphill”, 강한 단조감소(strictly decreasing)면 “Downhill”을 출력한다. 또한 높이가 일정하다면 “Flat Land”를 출력하고, 어느 경우에도 속하지 않으면 “Unknown”을 출력한다.<br /></p>	[{"input": "1\\n10\\n12\\n13\\n", "output": "Uphill"}]	595fb3de66e601bd39565b92ba606c9e	[{"score": 20, "input_name": "1.in", "output_name": "1.out"}, {"score": 20, "input_name": "2.in", "output_name": "2.out"}, {"score": 20, "input_name": "3.in", "output_name": "3.out"}, {"score": 20, "input_name": "4.in", "output_name": "4.out"}, {"score": 20, "input_name": "5.in", "output_name": "5.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 07:55:02.90826+00	\N	2000	512	f	\N	\N	\N	ACM	t	Low		0	0	1	A	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
13	회전 표지판	<p>예술가 민정이는 바람에 자유롭게 회전해도 알아볼 수 있는 표지판을 만들려고 한다.이러한 표지판을 만들기 위해 민정이는180도 회전해도 변하지 않는문자인H, I, N, O, S, X, Z만을 사용할 수 있다.</p><p>단어를 보고,그 단어가 회전 표지판­에 사용될 수 있는지를 결정하는 프로그램을 작성하라.</p>	<p>공백 없이 알파벳 대문자로만 이루어진 하나의 문자열 S가 주어진다.문자열의 길이는30을 넘지 않는다.<br /></p>	<p>단어 S가 회전 표지판에 사용될 수 있다면YES를,사용될 수 없다면NO를 출력한다.<br /></p>	[{"input": "SHINS", "output": "YES"}, {"input": "NO", "output": "YES"}, {"input": "SHOW", "output": "NO"}]	43bc2af24c18f0948bab7fb0e77b5d98	[{"score": 10, "input_name": "1.in", "output_name": "1.out"}, {"score": 10, "input_name": "2.in", "output_name": "2.out"}, {"score": 10, "input_name": "3.in", "output_name": "3.out"}, {"score": 10, "input_name": "4.in", "output_name": "4.out"}, {"score": 10, "input_name": "5.in", "output_name": "5.out"}, {"score": 10, "input_name": "6.in", "output_name": "6.out"}, {"score": 10, "input_name": "7.in", "output_name": "7.out"}, {"score": 10, "input_name": "8.in", "output_name": "8.out"}, {"score": 10, "input_name": "9.in", "output_name": "9.out"}, {"score": 10, "input_name": "10.in", "output_name": "10.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 12:09:36.643292+00	\N	1000	128	f	\N	\N	\N	ACM	t	Low		0	0	1	B	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
14	붕어빵	<p>겨울이 되어 길거리 곳곳에서 붕어빵을 팔고 있다.성균이가 운영하는 붕어빵 가게 앞에는 N명의 손님이 한 줄로 서 있다.각 손님은 $a_i$개의 붕어빵을 사려고 한다.</p><p>성균이는 같은 개수의 붕어빵을 구매하는 손님들이 연속되어 있으면 담는게 더 수월하리라 생각한다.따라서 특정 손님을 정하고,그 손님이 사려고 하는 붕어빵의 개수와 같은 개수의 붕어빵을 사려고 하는 손님들을 줄에서 모두 내보내려고 한다.</p><p>어떤 특정 개수의 붕어빵을 사려고 하는 사람들을 줄에서 내보내야,같은 개수의 붕어빵을 사려고 하는 사람들이 연속된 구간 중 가장 긴 것의 길이가 최대가 되는지 구하는 프로그램을 작성하라.</p>	<p>첫째 줄에 손님 수 $N$이 주어진다. $(1 \\le N \\le 1000)$ 둘째 줄부터 $N$개의 줄에 걸쳐 가게 앞에 서 있는 순서대로 각 손님이 사려고 하는 붕어빵의 개수 $a_i$가 주어진다. $(0\\le a_i \\le 1,000,000)$ 항상 두 개 이상의 서로 다른 $a_i$가 존재한다.<br /></p>	<p>성균이가 만들 수 있는 같은 개수의 붕어빵을 원하는 손님들의 연속된 구간 중,가장 긴 것의 길이를 출력한다.<br /></p>	[{"input": "9\\n2\\n7\\n3\\n7\\n7\\n3\\n7\\n5\\n7\\n", "output": "4"}]	2fba6fa050bc13a581b05ce29264cec0	[{"score": 5, "input_name": "1.in", "output_name": "1.out"}, {"score": 5, "input_name": "2.in", "output_name": "2.out"}, {"score": 5, "input_name": "3.in", "output_name": "3.out"}, {"score": 5, "input_name": "4.in", "output_name": "4.out"}, {"score": 5, "input_name": "5.in", "output_name": "5.out"}, {"score": 5, "input_name": "6.in", "output_name": "6.out"}, {"score": 5, "input_name": "7.in", "output_name": "7.out"}, {"score": 5, "input_name": "8.in", "output_name": "8.out"}, {"score": 5, "input_name": "9.in", "output_name": "9.out"}, {"score": 5, "input_name": "10.in", "output_name": "10.out"}, {"score": 5, "input_name": "11.in", "output_name": "11.out"}, {"score": 5, "input_name": "12.in", "output_name": "12.out"}, {"score": 5, "input_name": "13.in", "output_name": "13.out"}, {"score": 5, "input_name": "14.in", "output_name": "14.out"}, {"score": 5, "input_name": "15.in", "output_name": "15.out"}, {"score": 5, "input_name": "16.in", "output_name": "16.out"}, {"score": 5, "input_name": "17.in", "output_name": "17.out"}, {"score": 5, "input_name": "18.in", "output_name": "18.out"}, {"score": 5, "input_name": "19.in", "output_name": "19.out"}, {"score": 5, "input_name": "20.in", "output_name": "20.out"}, {"score": 5, "input_name": "21.in", "output_name": "21.out"}, {"score": 5, "input_name": "22.in", "output_name": "22.out"}]	<p>줄에 서 있는9명의 손님들이 사려고 하는 붕어빵의 개수는2, 7, 3, 7, 7, 3, 7, 5, 7이다.</p><p>3개를 사려고 하는 사람을 줄에서 내보내면,줄은2, 7, 7, 7, 7, 5, 7이 된다.이 때7개를 사려고 하는 사람4명이 연속된 구간이 가장 길이가 긴 구간이다.</p>	["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 12:15:17.912225+00	\N	1000	128	f	\N	\N	\N	ACM	t	Mid		0	0	1	C	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
15	채권관계	<p>드디어 동아리방이 생긴NPC는 동아리방 물품을 구입하는 데 한창이다.돈에는 신경쓰지 않고 물품 구입에 너무나 열중한 나머지, NPC부원들이 서로에게 빚을 졌다. NPC에서 돈을 갚을 때에는 자신과 친분 관계에 있는 사람한테만 돈을 갚을 수 있다.다음 학기 활동 전에는 모든 사람의 빚을 없애야 정상적인 활동이 가능하기에,빚을 없애는 것이 가능한지 확인하려고 한다.<br /></p>	<p>첫째 줄에는 각각 동아리 부원 수, 친분 관계의 수를 나타내는 두 개의 정수 $N(2 \\le N \\le 10,000)$, $M(0 \\le M \\le 50,000)$이 주어진다.</p><p>둘째 줄부터 N개의 줄에 걸쳐 각 사람이 갚거나 받아야 하는 돈을 나타내는 정수 $K(-10,000 \\le K \\le 10,000)$가 주어진다. $K \\lt 0$인 경우는 빚을 졌다는 뜻이다. $N$개의 정수 $K$의 합은 0이다.</p><p>이어서 $M$개의 줄에 걸쳐 두 개의 정수 $x, y (0 \\lt x \\lt y \\le N–1)$가 주어지며, $x, y$는 서로 친분 관계이다.</p>	<p>모든 사람의 빚을 없애는 것이 가능하면“POSSIBLE”,불가능하면“IMPOSSIBLE”을 출력한다.<br /></p>	[{"input": "5 3\\n100\\n-75\\n-25\\n-42\\n42\\n0 1\\n1 2\\n3 4\\n", "output": "POSSIBLE"}]	a2d3795ff003735ec5be7a155a732775	[{"score": 11, "input_name": "1.in", "output_name": "1.out"}, {"score": 11, "input_name": "2.in", "output_name": "2.out"}, {"score": 11, "input_name": "3.in", "output_name": "3.out"}, {"score": 11, "input_name": "4.in", "output_name": "4.out"}, {"score": 11, "input_name": "5.in", "output_name": "5.out"}, {"score": 11, "input_name": "6.in", "output_name": "6.out"}, {"score": 11, "input_name": "7.in", "output_name": "7.out"}, {"score": 11, "input_name": "8.in", "output_name": "8.out"}, {"score": 11, "input_name": "9.in", "output_name": "9.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 12:22:26.113175+00	\N	1000	256	f	\N	\N	\N	ACM	t	Low		0	0	1	D	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
16	타일 교환	<p>민수는 최근에 마트에서 구입한 정사각형 타일들을 사용하여 동아리방 바닥을 리모델링하려고 한다. 하지만 민수는 구입하기 전에 연구실의 크기를 제대로 측정하지 않아, 타일 중 일부를 다른 크기의 새로운 정사각형 타일들로 교환해야 한다.</p><p>민수가 구매한 $N$개의 정사각형 타일들의 길이는 각각 $a_1…a_N$이다. 민수는 타일들의 총면적이 $M$이 되도록 이들 중 일부를 새로운 정사각형 타일로 교환하려 한다.</p><p>때마침 마트에서 현재 특별 이벤트를 진행해서, 길이 $a_i$의 타일을 길이 $b_i$로 변경할 때 $|a_i-b_i |^2$ 만큼의 비용을 지불하면 된다. 그러나 이 이벤트는 직접 구입한 타일에만 적용되기 때문에 다른 타일을 교환하여 얻은 타일은 교환할 수 없다.</p><p>이때, 타일들의 총면적이 $M$이 되도록 타일 교환을 하는 데에 필요한 최소 비용을 구하는 프로그램을 작성하라.</p>	<p>첫째 줄에 $N(1 \\le N \\le 10)$과 $M(1 \\le M \\le 10,000)$이 주어진다.</p><p>둘째 줄부터 $N$개의 줄에 걸쳐 각 정사각형 타일의 길이 $a_i (1 \\le a_i \\le 100)$가 주어진다.</p>	<p>총면적이 $M$이 되도록 하는 타일 교환의 최소 비용을 출력한다. 총면적이 $M$이 될 수 없는 경우는 -1을 출력한다.<br /></p>	[{"input": "3 6\\n3\\n3\\n1\\n", "output": "5"}]	ea7df202570834f1fc5700228e811c8e	[{"score": 8, "input_name": "1.in", "output_name": "1.out"}, {"score": 8, "input_name": "2.in", "output_name": "2.out"}, {"score": 8, "input_name": "3.in", "output_name": "3.out"}, {"score": 8, "input_name": "4.in", "output_name": "4.out"}, {"score": 8, "input_name": "5.in", "output_name": "5.out"}, {"score": 8, "input_name": "6.in", "output_name": "6.out"}, {"score": 8, "input_name": "7.in", "output_name": "7.out"}, {"score": 8, "input_name": "8.in", "output_name": "8.out"}, {"score": 8, "input_name": "9.in", "output_name": "9.out"}, {"score": 8, "input_name": "10.in", "output_name": "10.out"}, {"score": 8, "input_name": "11.in", "output_name": "11.out"}, {"score": 8, "input_name": "12.in", "output_name": "12.out"}]	<p>3개의 타일이 있고,두개의 타일은 길이가3인 정사각형이고,한 개의 타일은 길이가1인 정사각형이다.이것들을 총면적이6이 되도록 교환하려 한다.</p><p>길이가3인 정사각형 중 하나를 길이가2인 정사각형으로 바꾸고,길이가3인 나머지 정사각형 하나를 길이가1인 정사각형으로 바꾼다.이렇게 하면 원하는 면적4+1+1=6을 얻을 수 있으며 교환 비용은4+1=5이다.</p>	["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 12:27:07.606365+00	\N	1000	128	f	\N	\N	\N	ACM	t	Mid		0	0	1	E	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
17	천재 디자이너	<p>프리랜서로 일하는 디자이너 지환이는 일렬로 이어진 $N$개의 칸을 색칠해달라는 클라이언트의 요청을 받았다. 지환이는 열심히 색을 골라서 색 조합을 클라이언트에게 전송했고, 스스로가 생각하기에도 이번 디자인은 정말 잘 뽑힌 것 같았다. 이번 외주도 별문제 없이 해결했을거로 생각한 지환이는 오랜 시간 동안 고민해오던 시력 교정 수술을 예약했다. 평소에 마스크를 끼면 자꾸 안경에 김이 서려서 화가 났었기 때문이다.</p><p>수술 후에 클라이언트의 연락을 받은 지환이는 생각보다 너무나도 까다로운 클라이언트의 피드백에 놀라지 않을 수 없었다. 클라이언트는 총 $Q$개의 구간을 제시했다. 그리고 그 $Q$개의 구간 안에서는 각 칸이 모두 다른 색으로 구성되었으면 좋겠다고 말했다. 지환이는 마음속으로 “진작 이렇게 말하지…” 라는 생각을 했지만 금방 수정본을 만들어서 보내겠다고 말했다.</p><p>문제는 시력 교정 수술이었다. 안과에서는 자외선을 조심하라고 말했지만, 지환이는 이를 모니터 화면을 보면 안 된다고 오해하고 있던 것이다. 화면을 안 보고 디자인을 수정할 수는 없지만, 치환이는 천재 디자이너였기 때문에 자신의 디자인을 어느 정도 기억하고 있었다.</p><p>지환이는 자신이 지금까지 쓴 색들이 무엇인지와, 어떤 위치에 있는 색이 마음에 들었는지를 기억하고 있었고, 마음에 안 드는 색부터 지금까지 쓰지 않은 새로운 색으로 하나씩 수정하여 클라이언트에게 수정본을 보내야겠다고 생각했다.</p><p>이때, 지환이가 몇 번째 수정본에서 클라이언트가 만족하는 디자인을 만들 수 있을지를 출력하라.</p>	<p>첫째 줄에는 알파벳 소문자로 이루어진 $N (1 \\le N \\le 10^5)$개의 색이 문자열로 주어진다.</p><p>둘째 줄에는 구간의 개수 $Q (1 \\le Q \\le 10^5)$가 주어진다.</p><p>그 다음 $Q$개의 줄에 걸쳐 각 구간이 $a_i$와 $b_i$로 주어진다. $(1 \\le a_i \\le b_i \\le N)$ 이는 $a_i$번째 칸부터 $b_i$번째 칸까지의 구간을 의미한다.</p><p>마지막 줄에는 지환이가 초안에서 마음에 들지 않았던 색부터 가장 마음에 드는 위치까지 총 $N$개의 서로 다른 칸의 위치가 주어진다.</p>	<p>몇 번째 수정본에서 클라이언트가 만족하는 디자인을 만들 수 있을지0이상의 정수로 출력한다.<br /></p>	[{"input": "aaaaa\\n2\\n1 2\\n4 5\\n2 4 1 5 3\\n", "output": "2"}, {"input": "abbabaab\\n3\\n1 3\\n4 7\\n3 5\\n6 3 5 1 4 2 7 8\\n", "output": "5"}, {"input": "abcd\\n1\\n1 4\\n1 2 3 4\\n", "output": "0"}]	46d110d202d1fef9c7ece9ad1a1ec351	[{"score": 3, "input_name": "1.in", "output_name": "1.out"}, {"score": 3, "input_name": "2.in", "output_name": "2.out"}, {"score": 3, "input_name": "3.in", "output_name": "3.out"}, {"score": 3, "input_name": "4.in", "output_name": "4.out"}, {"score": 3, "input_name": "5.in", "output_name": "5.out"}, {"score": 3, "input_name": "6.in", "output_name": "6.out"}, {"score": 3, "input_name": "7.in", "output_name": "7.out"}, {"score": 3, "input_name": "8.in", "output_name": "8.out"}, {"score": 3, "input_name": "9.in", "output_name": "9.out"}, {"score": 3, "input_name": "10.in", "output_name": "10.out"}, {"score": 3, "input_name": "11.in", "output_name": "11.out"}, {"score": 3, "input_name": "12.in", "output_name": "12.out"}, {"score": 3, "input_name": "13.in", "output_name": "13.out"}, {"score": 3, "input_name": "14.in", "output_name": "14.out"}, {"score": 3, "input_name": "15.in", "output_name": "15.out"}, {"score": 3, "input_name": "16.in", "output_name": "16.out"}, {"score": 3, "input_name": "17.in", "output_name": "17.out"}, {"score": 3, "input_name": "18.in", "output_name": "18.out"}, {"score": 3, "input_name": "19.in", "output_name": "19.out"}, {"score": 3, "input_name": "20.in", "output_name": "20.out"}, {"score": 3, "input_name": "21.in", "output_name": "21.out"}, {"score": 3, "input_name": "22.in", "output_name": "22.out"}, {"score": 3, "input_name": "23.in", "output_name": "23.out"}, {"score": 3, "input_name": "24.in", "output_name": "24.out"}, {"score": 3, "input_name": "25.in", "output_name": "25.out"}, {"score": 3, "input_name": "26.in", "output_name": "26.out"}, {"score": 3, "input_name": "27.in", "output_name": "27.out"}, {"score": 3, "input_name": "28.in", "output_name": "28.out"}, {"score": 3, "input_name": "29.in", "output_name": "29.out"}, {"score": 3, "input_name": "30.in", "output_name": "30.out"}, {"score": 3, "input_name": "31.in", "output_name": "31.out"}]		["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 12:32:42.267502+00	\N	2000	512	f	\N	\N	\N	ACM	t	High		0	0	1	F	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
20	사이클 분할	<p>가중치가 있는 무방향 간선들로 이루어진 $N$개의 정점의 완전 그래프가 있다. ($N$은 홀수)</p><p>$K$개의 간선들로 이루어진 배열 $[e_1,e_2,…,e_K ]$을 ‘사이클 배열’이라 하고, 다음을 만족한다고 하자.</p><ul><li>$K \\lt1$</li><li>임의의 $i$ $(1 \\le i \\le k)$에 대해 간선 $e_i$는 $e_{i-1}$과 정확히 하나의 정점을 공유하고 $e_{i+1}$과도 정확히 하나의 정점을 공유하며, 이 정점들은 서로 다르다. ($e_0=e_k$, $e_1=e_{k+1}$로 간주한다)</li></ul><p>‘사이클 배열’의 간선들이 사이클을 형성함은 명백하다.</p><p>함수 $f(e_1, e_2 )$는 간선 $e_1, e_2$를 매개변수로 취하고 $e_1$과 $e_2$의 가중치 중 최대값을 반환하는 것으로 정의한다.</p><p>‘사이클 배열’ $C=[e_1, e_2, …, e_K ]$에 대해, ‘사이클 배열의 비용’을 1과 $K$ 사이 모든 $i$에 대한 $f(e_i, e_{i+1} )$의 합으로 정의하자. ($e_1=e_{K+1}$로 간주한다)</p><p>그래프에 대한 ‘사이클 분할’을 교집합이 없는 ‘사이클 배열’들의 집합으로 정의하자. ‘사이클 분할’의 원소들의 합집합은 그래프의 모든 간선들을 포함해야 한다. ‘사이클 분할의 비용’을 ‘사이클 분할’에 포함되어 있는 ‘사이클 배열’들의 비용의 합으로 정의하자.</p><p>하나의 그래프에 대해 다양한 ‘사이클 분할’이 존재할 수 있을 것이다. 그래프가 주어지면, 가장 비용이 낮은 사이클 분할을 찾고, 그 비용을 출력하는 프로그램을 작성하라.</p>	<p>첫째 줄에 정점의 개수 N이 주어진다. ($3 \\le N \\lt 1,000$, $N$은 홀수)</p><p>둘째 줄부터 $\\frac{N∙(N-1)}{2} $개의 줄에는 세 정수 $u,v,w$ $(1 \\le u, v \\le N, u \\ne v, 1 \\le w \\le 10^9 )$가 주어진다. 정점 $u$와 정점 $v$ 사이에 가중치 $w$의 간선이 있다는 뜻이다.</p>	<p>첫째 줄에 그래프에 대한 ‘사이클 분할의 비용’의 최솟값을 하나의 정수로 출력한다.<br /></p>	[{"input": "3\\n1 2 1\\n2 3 1\\n3 1 1", "output": "3"}, {"input": "5\\n4 5 4\\n1 3 4\\n1 2 4\\n3 2 3\\n3 5 2\\n1 4 3\\n4 2 2\\n1 5 4\\n5 2 4\\n3 4 2", "output": "35"}]	d7784a8aafc47330e4311baa7d3e07cd	[{"score": 5, "input_name": "1.in", "output_name": "1.out"}, {"score": 5, "input_name": "2.in", "output_name": "2.out"}, {"score": 5, "input_name": "3.in", "output_name": "3.out"}, {"score": 5, "input_name": "4.in", "output_name": "4.out"}, {"score": 5, "input_name": "5.in", "output_name": "5.out"}, {"score": 5, "input_name": "6.in", "output_name": "6.out"}, {"score": 5, "input_name": "7.in", "output_name": "7.out"}, {"score": 5, "input_name": "8.in", "output_name": "8.out"}, {"score": 5, "input_name": "9.in", "output_name": "9.out"}, {"score": 5, "input_name": "10.in", "output_name": "10.out"}, {"score": 5, "input_name": "11.in", "output_name": "11.out"}, {"score": 5, "input_name": "12.in", "output_name": "12.out"}, {"score": 5, "input_name": "13.in", "output_name": "13.out"}, {"score": 5, "input_name": "14.in", "output_name": "14.out"}, {"score": 5, "input_name": "15.in", "output_name": "15.out"}, {"score": 5, "input_name": "16.in", "output_name": "16.out"}, {"score": 5, "input_name": "17.in", "output_name": "17.out"}, {"score": 5, "input_name": "18.in", "output_name": "18.out"}, {"score": 5, "input_name": "19.in", "output_name": "19.out"}]	<p>예제에서 입력되는 순서대로 간선에 번호를 매겨보자. $i$번째 간선을 $e_i$라고 하자.</p><p>첫 번째 예제에서 유일하게 가능한 사이클 분할은 $S=\\{[e_1,e_2,e_3 ]\\}$이다. $f(e_1,e_2 ) + f(e_2,e_3 ) + f(e_3,e_1 ) = 1+1+1=3$</p><p>두 번째 예제에서 최적의 사이클 분할은 $S=\\{[e_3,e_8,e_9 ],[e_2,e_4,e_7,e_{10},e_5,e_1,e_6 ]\\}$이다. $[e_3,e_8,e_9 ]$의 비용은 12이고, $[e_2,e_4,e_7,e_{10},e_5,e_1,e_6 ]$의 가격은 23이다. 따라서 사이클 분할의 가격은 35이다.</p>	["C", "C++", "Golang", "Java", "Python2", "Python3"]	{}	2021-01-02 14:44:26.25011+00	\N	2000	256	f	\N	\N	\N	ACM	t	High		0	0	1	G	{}	0	2	f	f	{"input": "input.txt", "output": "output.txt", "io_mode": "Standard IO"}	f
\.


--
-- Data for Name: problem_tag; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.problem_tag (id, name) FROM stdin;
1	Condition
2	test
3	123
4	Bronze
5	tag
6	TEST
\.


--
-- Data for Name: problem_tags; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.problem_tags (id, problem_id, problemtag_id) FROM stdin;
29	10	2
34	12	2
36	6	4
37	13	2
38	14	2
39	15	2
40	16	2
41	17	2
45	20	2
\.


--
-- Data for Name: submission; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.submission (id, contest_id, problem_id, create_time, user_id, code, result, info, language, shared, statistic_info, username, ip) FROM stdin;
c0141f0441ea4e916ff1498f157c67a5	2	12	2021-01-02 13:23:05.049585+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int h[4];\n    for (int i = 0; i < 4; i++) {\n        cin >> h[i];\n    }\n    if (h[0] < h[1] && h[1] < h[2] && h[2] < h[3]) {\n        cout << "Uphill" << endl;\n    } else if (h[0] > h[1] && h[1] > h[2] && h[2] > h[3]) {\n        cout << "Downhill" << endl;\n    } else if (h[0] == h[1] && h[1] == h[2] && h[2] == h[3]) {\n        cout << "Flat Land" << endl;\n    } else {\n        cout << "Unknown" << endl;\n    }\n}	0	{"err": null, "data": [{"error": 0, "memory": 3538944, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "fb17f4489a9c61e0ac6f91a2c273c385"}, {"error": 0, "memory": 3514368, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}, {"error": 0, "memory": 3428352, "output": null, "result": 0, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "88183b946cc5f0e8c96b2e66e1c74a7e"}, {"error": 0, "memory": 3547136, "output": null, "result": 0, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "6dd08fe20654d741a880b5121aff195e"}, {"error": 0, "memory": 3416064, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "88183b946cc5f0e8c96b2e66e1c74a7e"}]}	C++	f	{"time_cost": 2, "memory_cost": 3547136}	root	116.34.23.161
8a8db7953d844f77f0688b31ce0c7181	2	12	2021-01-02 13:56:59.436599+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int arr[5];\n    arr[0] = arr[1] + arr[1000000];\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3489792, "output": null, "result": -1, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3407872, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3461120, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3358720, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3293184, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}]}	C++	f	{"time_cost": 2, "memory_cost": 3489792}	root	116.34.23.161
4537a9ed4d87217a9453d84b1db6397d	2	12	2021-01-02 13:58:04.117953+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int arr[5];\n    arr[0] = arr[1] + arr[90000000];\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3444736, "output": null, "result": -1, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3440640, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3469312, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3448832, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3403776, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 1, "test_case": "5", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}]}	C++	f	{"time_cost": 2, "memory_cost": 3469312}	root	116.34.23.161
b51e33853781a8c8f44a433e94066145	2	12	2021-01-02 13:59:48.377003+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint arr[INT_MAX];\n\nint main() {\n    int a = 1 + 2;\n    int b[50];\n}	-2	{}	C++	f	{"score": 0, "err_info": "/tmp/ccTV4UpA.o: In function `_GLOBAL__sub_I_arr':\\nmain.cpp:(.text.startup+0x13): relocation truncated to fit: R_X86_64_PC32 against `.bss'\\nmain.cpp:(.text.startup+0x31): relocation truncated to fit: R_X86_64_PC32 against `.bss'\\ncollect2: error: ld returned 1 exit status"}	root	116.34.23.161
7ce5c52306ffcff515976567b4227b80	2	13	2021-01-02 14:05:50.160804+00	1	#include <iostream>\nusing namespace std;\n\nint main() {\n    string s;\n    string aval = "IOSHZXN";\n\n    cin >> s;\n    \n    for (char &i : s) {\n        if (aval.find(i) == -1) {\n            cout << "NO" << endl;\n            return 0;\n        }\n    }\n\n    cout << "YES" << endl;\n}	0	{"err": null, "data": [{"error": 0, "memory": 3444736, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "c2f3f489a00553e7a01d369c103c7251"}, {"error": 0, "memory": 3289088, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "7469a286259799e5b37e5db9296f00b3"}, {"error": 0, "memory": 3444736, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "7469a286259799e5b37e5db9296f00b3"}, {"error": 0, "memory": 3444736, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "4", "output_md5": "c2f3f489a00553e7a01d369c103c7251"}, {"error": 0, "memory": 3604480, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "c2f3f489a00553e7a01d369c103c7251"}, {"error": 0, "memory": 3522560, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "6", "output_md5": "7469a286259799e5b37e5db9296f00b3"}, {"error": 0, "memory": 3461120, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "7", "output_md5": "7469a286259799e5b37e5db9296f00b3"}, {"error": 0, "memory": 3461120, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "8", "output_md5": "c2f3f489a00553e7a01d369c103c7251"}, {"error": 0, "memory": 3493888, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "9", "output_md5": "7469a286259799e5b37e5db9296f00b3"}, {"error": 0, "memory": 3448832, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "10", "output_md5": "c2f3f489a00553e7a01d369c103c7251"}]}	C++	f	{"time_cost": 2, "memory_cost": 3604480}	root	116.34.23.161
72926615e07978cc7c1e69c2356ad509	2	12	2021-01-02 13:24:47.968696+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nvoid dfs() {\n    dfs();\n}\n\nint main() {\n    dfs();\n}	1	{"err": null, "data": [{"error": 0, "memory": 3043328, "output": null, "result": 1, "signal": 9, "cpu_time": 2996, "exit_code": 0, "real_time": 2997, "test_case": "1", "output_md5": null}, {"error": 0, "memory": 3039232, "output": null, "result": 1, "signal": 9, "cpu_time": 2992, "exit_code": 0, "real_time": 2998, "test_case": "2", "output_md5": null}, {"error": 0, "memory": 3207168, "output": null, "result": 1, "signal": 9, "cpu_time": 2992, "exit_code": 0, "real_time": 2998, "test_case": "3", "output_md5": null}, {"error": 0, "memory": 3198976, "output": null, "result": 1, "signal": 9, "cpu_time": 2992, "exit_code": 0, "real_time": 2998, "test_case": "4", "output_md5": null}, {"error": 0, "memory": 3080192, "output": null, "result": 1, "signal": 9, "cpu_time": 2992, "exit_code": 0, "real_time": 2997, "test_case": "5", "output_md5": null}]}	C++	f	{"time_cost": 2996, "memory_cost": 3207168}	root	116.34.23.161
f5c8dd4203c2175549356570dce4dee8	2	12	2021-01-02 13:57:46.358497+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int arr[5];\n    arr[0] = arr[1] + arr[1000000];\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3411968, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3297280, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3391488, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3448832, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 1, "test_case": "4", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3416064, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}]}	C++	f	{"time_cost": 1, "memory_cost": 3448832}	root	116.34.23.161
ade95e4d398edb22439cb6ab9a8d96fe	2	12	2021-01-02 13:58:13.699839+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int arr[5];\n    arr[0] = arr[1] + arr[900000000];\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3346432, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3321856, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3411968, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3416064, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3448832, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}]}	C++	f	{"time_cost": 1, "memory_cost": 3448832}	root	116.34.23.161
c5cfd7efc9d95ed51e8adc66a9ba2126	2	12	2021-01-02 14:01:50.489735+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int a = 1 / 0;\n    int b[50];\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3293184, "output": null, "result": -1, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3522560, "output": null, "result": -1, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3473408, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3473408, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}, {"error": 0, "memory": 3428352, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "d41d8cd98f00b204e9800998ecf8427e"}]}	C++	f	{"time_cost": 2, "memory_cost": 3522560}	root	116.34.23.161
6b925b5d298a9ecf4d0cc4089b4c34fd	2	12	2021-01-02 14:02:07.39093+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int a = 1 / 0;\n    int b[50];\n  \tcout << "Uphill" << endl;\n}	-1	{"err": null, "data": [{"error": 0, "memory": 3506176, "output": null, "result": -1, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 3, "test_case": "1", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}, {"error": 0, "memory": 3510272, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 2, "test_case": "2", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}, {"error": 0, "memory": 3506176, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "3", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}, {"error": 0, "memory": 3510272, "output": null, "result": -1, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}, {"error": 0, "memory": 3297280, "output": null, "result": -1, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "5", "output_md5": "1610e363a7085598cbb3f9ce5cb7732e"}]}	C++	f	{"time_cost": 2, "memory_cost": 3510272}	root	116.34.23.161
da4d26648cd4f54248135e4d1728dca8	2	12	2021-01-02 14:05:00.355807+00	1	#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    int h[4];\n    for (int i = 0; i < 4; i++) {\n        cin >> h[i];\n    }\n    if (h[0] < h[1] && h[1] < h[2] && h[2] < h[3]) {\n        cout << "Uphill" << endl;\n    } else if (h[0] > h[1] && h[1] > h[2] && h[2] > h[3]) {\n        cout << "Downhill" << endl;\n    } else if (h[0] == h[1] && h[1] == h[2] && h[2] == h[3]) {\n        cout << "Flat Land" << endl;\n    } else {\n        cout << "Unknown" << endl;\n    }\n  return 1;\n}	4	{"err": null, "data": [{"error": 0, "memory": 3526656, "output": null, "result": 4, "signal": 0, "cpu_time": 2, "exit_code": 1, "real_time": 2, "test_case": "1", "output_md5": null}, {"error": 0, "memory": 3514368, "output": null, "result": 4, "signal": 0, "cpu_time": 2, "exit_code": 1, "real_time": 3, "test_case": "2", "output_md5": null}, {"error": 0, "memory": 3543040, "output": null, "result": 4, "signal": 0, "cpu_time": 2, "exit_code": 1, "real_time": 2, "test_case": "3", "output_md5": null}, {"error": 0, "memory": 3411968, "output": null, "result": 4, "signal": 0, "cpu_time": 2, "exit_code": 1, "real_time": 3, "test_case": "4", "output_md5": null}, {"error": 0, "memory": 3411968, "output": null, "result": 4, "signal": 0, "cpu_time": 1, "exit_code": 1, "real_time": 2, "test_case": "5", "output_md5": null}]}	C++	f	{"time_cost": 2, "memory_cost": 3543040}	root	116.34.23.161
e9be56707653946b5bfc9cfbe941882e	2	14	2021-01-02 14:06:14.515598+00	1	#include <iostream>\n#include <vector>\nusing namespace std;\n\nint main() {\n    int n;\n    int ans = 0;\n    vector<int> v;\n\n    cin >> n;\n    v.resize(n);\n    for (auto &i : v) cin >> i;\n\n    for (const auto &skip : v) {\n        int cnt = 0;\n        int prev = -1;\n\n        for (const auto &j : v) {\n            if (j == skip) continue;\n\n            if (prev != j) {\n                prev = j;\n                ans = max(ans, cnt);\n                cnt = 1;\n            } else {\n                cnt++;\n            }\n        }\n\n        ans = max(ans, cnt);\n    }\n\n    cout << ans << endl;\n}	0	{"err": null, "data": [{"error": 0, "memory": 3461120, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "1", "output_md5": "a87ff679a2f3e71d9181a67b7542122c"}, {"error": 0, "memory": 3469312, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 5, "test_case": "2", "output_md5": "c4ca4238a0b923820dcc509a6f75849b"}, {"error": 0, "memory": 3391488, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "3", "output_md5": "a87ff679a2f3e71d9181a67b7542122c"}, {"error": 0, "memory": 3416064, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "4", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3395584, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 2, "test_case": "5", "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3"}, {"error": 0, "memory": 3473408, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "6", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3444736, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "7", "output_md5": "a87ff679a2f3e71d9181a67b7542122c"}, {"error": 0, "memory": 3395584, "output": null, "result": 0, "signal": 0, "cpu_time": 6, "exit_code": 0, "real_time": 6, "test_case": "8", "output_md5": "e4da3b7fbbce2345d7772b0674a318d5"}, {"error": 0, "memory": 3616768, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 5, "test_case": "9", "output_md5": "a87ff679a2f3e71d9181a67b7542122c"}, {"error": 0, "memory": 3317760, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 5, "test_case": "10", "output_md5": "a87ff679a2f3e71d9181a67b7542122c"}, {"error": 0, "memory": 3428352, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 5, "test_case": "11", "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3"}, {"error": 0, "memory": 3436544, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 5, "test_case": "12", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3297280, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 6, "test_case": "13", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3395584, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 6, "test_case": "14", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3530752, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 6, "test_case": "15", "output_md5": "53fde96fcc4b4ce72d7739202324cd49"}, {"error": 0, "memory": 3641344, "output": null, "result": 0, "signal": 0, "cpu_time": 5, "exit_code": 0, "real_time": 5, "test_case": "16", "output_md5": "c51ce410c124a10e0db5e4b97fc2af39"}, {"error": 0, "memory": 3465216, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 4, "test_case": "17", "output_md5": "eccbc87e4b5ce2fe28308fd9f2a7baf3"}, {"error": 0, "memory": 3645440, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 5, "test_case": "18", "output_md5": "8f14e45fceea167a5a36dedd4bea2543"}, {"error": 0, "memory": 3416064, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "19", "output_md5": "fbd7939d674997cdb4692d34de8633c4"}, {"error": 0, "memory": 3588096, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 3, "test_case": "20", "output_md5": "66f041e16a60928b05a7e228a89c3799"}, {"error": 0, "memory": 3436544, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "21", "output_md5": "9a1158154dfa42caddbd0694a4e9bdc8"}, {"error": 0, "memory": 3612672, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 5, "test_case": "22", "output_md5": "9a1158154dfa42caddbd0694a4e9bdc8"}]}	C++	f	{"time_cost": 6, "memory_cost": 3645440}	root	116.34.23.161
c95d9b5ba915b5e843b8518864ad22ec	2	15	2021-01-02 14:06:56.64548+00	1	#include <iostream>\n#include <vector>\nusing namespace std;\n\nint n, m;\nint cost[10005];\nbool check[10005];\nvector<int> adj[10005];\n\nint dfs(int curr) {\n    int sum = cost[curr];\n    check[curr] = true;\n\n    for (const auto &nxt : adj[curr]) {\n        if (!check[nxt]) {\n            sum += dfs(nxt);\n        }\n    }\n\n    return sum;\n}\n\nint main() {\n    cin >> n >> m;\n\n    for (int i = 0; i < n; i++) {\n        cin >> cost[i];\n    }\n\n    for (int i = 0; i < m; i++) {\n        int u, v;\n        cin >> u >> v;\n        adj[u].push_back(v);\n        adj[v].push_back(u);        \n    }\n\n    for (int i = 0; i < n; i++) {\n        if (!check[i]) {\n            if (dfs(i) != 0) {\n                cout << "IMPOSSIBLE" << endl;\n                return 0;\n            }\n        }\n    }\n\n    cout << "POSSIBLE" << endl;\n}	0	{"err": null, "data": [{"error": 0, "memory": 4157440, "output": null, "result": 0, "signal": 0, "cpu_time": 12, "exit_code": 0, "real_time": 17, "test_case": "1", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 4259840, "output": null, "result": 0, "signal": 0, "cpu_time": 14, "exit_code": 0, "real_time": 19, "test_case": "2", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 4173824, "output": null, "result": 0, "signal": 0, "cpu_time": 7, "exit_code": 0, "real_time": 10, "test_case": "3", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 4411392, "output": null, "result": 0, "signal": 0, "cpu_time": 16, "exit_code": 0, "real_time": 21, "test_case": "4", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 3989504, "output": null, "result": 0, "signal": 0, "cpu_time": 6, "exit_code": 0, "real_time": 11, "test_case": "5", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 3923968, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 7, "test_case": "6", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 4235264, "output": null, "result": 0, "signal": 0, "cpu_time": 15, "exit_code": 0, "real_time": 16, "test_case": "7", "output_md5": "e23b33dee677e4477f0f7ddeb6cf87bd"}, {"error": 0, "memory": 3936256, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 6, "test_case": "8", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}, {"error": 0, "memory": 4120576, "output": null, "result": 0, "signal": 0, "cpu_time": 11, "exit_code": 0, "real_time": 15, "test_case": "9", "output_md5": "06fa6f806a3b83d883902d3f53b0b942"}]}	C++	f	{"time_cost": 16, "memory_cost": 4411392}	root	116.34.23.161
4a744c9871a8448ed77f7c1e5801e8e8	2	16	2021-01-02 14:07:26.567853+00	1	#include <iostream>\nusing namespace std;\n\nint n, m;\nint dp[11][10005];\nconst int INF = 987654321;\n\nint main() {\n    cin >> n >> m;\n\n    fill_n(&dp[0][0], 11 * 10005, INF);\n    dp[0][0] = 0;\n\n    for (int i = 1; i <= n; i++) {\n        int a;\n        cin >> a;\n\n        for (int j = 1; j * j <= m; j++) {\n            int cost = abs(a - j) * abs(a - j);\n\n            for (int k = j * j; k <= m; k++) {\n                dp[i][k] = min(dp[i][k], dp[i - 1][k - j * j] + cost);\n            }\n        }\n    }\n\n    cout << (dp[n][m] == INF ? -1 : dp[n][m]) << endl;\n}	0	{"err": null, "data": [{"error": 0, "memory": 3923968, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "1", "output_md5": "e4da3b7fbbce2345d7772b0674a318d5"}, {"error": 0, "memory": 3940352, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 4, "test_case": "2", "output_md5": "d58072be2820e8682c0a27c0518e805e"}, {"error": 0, "memory": 3809280, "output": null, "result": 0, "signal": 0, "cpu_time": 9, "exit_code": 0, "real_time": 9, "test_case": "3", "output_md5": "a97f6e2fedcabc887911dc9b5fd3ccc3"}, {"error": 0, "memory": 3809280, "output": null, "result": 0, "signal": 0, "cpu_time": 9, "exit_code": 0, "real_time": 10, "test_case": "4", "output_md5": "a3ec6dd8d538712a581e5b24726ce062"}, {"error": 0, "memory": 3796992, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "5", "output_md5": "6bb61e3b7bce0931da574d19d1d82c88"}, {"error": 0, "memory": 3956736, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 3, "test_case": "6", "output_md5": "6512bd43d9caa6e02c990b0a82652dca"}, {"error": 0, "memory": 3919872, "output": null, "result": 0, "signal": 0, "cpu_time": 1, "exit_code": 0, "real_time": 2, "test_case": "7", "output_md5": "3c59dc048e8850243be8079a5c74d079"}, {"error": 0, "memory": 3969024, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "8", "output_md5": "3c59dc048e8850243be8079a5c74d079"}, {"error": 0, "memory": 3960832, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 3, "test_case": "9", "output_md5": "c0c7c76d30bd3dcaefc96f40275bdc0a"}, {"error": 0, "memory": 3801088, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "10", "output_md5": "65b9eea6e1cc6bb9f0cd2a47751a186f"}, {"error": 0, "memory": 3973120, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 5, "test_case": "11", "output_md5": "ac2a728f9f17b5d860b6dabd80a5162f"}, {"error": 0, "memory": 3780608, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 7, "test_case": "12", "output_md5": "fb4ab556bc42d6f0ee0f9e24ec4d1af0"}]}	C++	f	{"time_cost": 9, "memory_cost": 3973120}	root	116.34.23.161
23087eaa0f5299479b3d120bdba1ee6f	2	17	2021-01-02 14:08:05.301895+00	1	#include <iostream>\nusing namespace std;\n\nint n, q;\nstring s;\nint l[100005];\nint r[100005];\nint t[100005];\nint cnt[26][100005];\n\nbool check(int x) {\n    for (int i = 0; i < 26; i++) {\n        for (int j = 1; j <= n; j++) {\n            cnt[i][j] = cnt[i][j - 1];\n\n            if (s[j - 1] == 'a' + i && t[j] > x) {\n                cnt[i][j]++;\n            }\n        }\n    }\n\n    for (int i = 0; i < 26; i++) {\n        for (int j = 0; j < q; j++) {\n            if (cnt[i][r[j]] - cnt[i][l[j] - 1] > 1) {\n                return false;\n            }\n        }\n    }\n\n    return true;\n}\n\nint main() {\n    cin >> s;\n    n = s.length();\n\n    cin >> q;\n\n    for (int i = 0; i < q; i++) {\n        cin >> l[i] >> r[i];\n    }\n\n    for (int i = 1; i <= n; i++) {\n        int p;\n        cin >> p;\n        t[p] = i;\n    }\n\n    int lo = 0;\n    int hi = n;\n\n    while (lo < hi) {\n        int mid = (lo + hi) / 2;\n        \n        if (check(mid)) {\n            hi = mid;\n        } else {\n            lo = mid + 1;\n        }\n    }\n\n    cout << lo << endl;\n}	0	{"err": null, "data": [{"error": 0, "memory": 3706880, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "1", "output_md5": "c81e728d9d4c2f636f067f89cc14862c"}, {"error": 0, "memory": 3723264, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "2", "output_md5": "e4da3b7fbbce2345d7772b0674a318d5"}, {"error": 0, "memory": 3633152, "output": null, "result": 0, "signal": 0, "cpu_time": 0, "exit_code": 0, "real_time": 3, "test_case": "3", "output_md5": "cfcd208495d565ef66e7dff9f98764da"}, {"error": 0, "memory": 15327232, "output": null, "result": 0, "signal": 0, "cpu_time": 167, "exit_code": 0, "real_time": 169, "test_case": "4", "output_md5": "023fcbb6cc093f6f06e0cfcb02565a48"}, {"error": 0, "memory": 15245312, "output": null, "result": 0, "signal": 0, "cpu_time": 158, "exit_code": 0, "real_time": 175, "test_case": "5", "output_md5": "d800c6cf5d304e013ec4f95ab772d62e"}, {"error": 0, "memory": 15167488, "output": null, "result": 0, "signal": 0, "cpu_time": 138, "exit_code": 0, "real_time": 143, "test_case": "6", "output_md5": "d3eb9a9233e52948740d7eb8c3062d14"}, {"error": 0, "memory": 3756032, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 3, "test_case": "7", "output_md5": "34ed066df378efacc9b924ec161e7639"}, {"error": 0, "memory": 3653632, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 5, "test_case": "8", "output_md5": "7fe1f8abaad094e0b5cb1b01d712f708"}, {"error": 0, "memory": 3670016, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "9", "output_md5": "3cf166c6b73f030b4f67eeaeba301103"}, {"error": 0, "memory": 3706880, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 4, "test_case": "10", "output_md5": "8dd48d6a2e2cad213179a3992c0be53c"}, {"error": 0, "memory": 3760128, "output": null, "result": 0, "signal": 0, "cpu_time": 2, "exit_code": 0, "real_time": 3, "test_case": "11", "output_md5": "019d385eb67632a7e958e23f24bd07d7"}, {"error": 0, "memory": 3670016, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 3, "test_case": "12", "output_md5": "05f971b5ec196b8c65b75d2ef8267331"}, {"error": 0, "memory": 3997696, "output": null, "result": 0, "signal": 0, "cpu_time": 8, "exit_code": 0, "real_time": 8, "test_case": "13", "output_md5": "8d9fc2308c8f28d2a7d2f6f48801c705"}, {"error": 0, "memory": 3948544, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 9, "test_case": "14", "output_md5": "ac5dab2e99eee9cf9ec672e383691302"}, {"error": 0, "memory": 3899392, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 7, "test_case": "15", "output_md5": "a36e841c5230a79c2102036d2e259848"}, {"error": 0, "memory": 3891200, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 8, "test_case": "16", "output_md5": "90599c8fdd2f6e7a03ad173e2f535751"}, {"error": 0, "memory": 3969024, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 8, "test_case": "17", "output_md5": "15d185eaa7c954e77f5343d941e25fbd"}, {"error": 0, "memory": 3952640, "output": null, "result": 0, "signal": 0, "cpu_time": 4, "exit_code": 0, "real_time": 9, "test_case": "18", "output_md5": "a36e841c5230a79c2102036d2e259848"}, {"error": 0, "memory": 4042752, "output": null, "result": 0, "signal": 0, "cpu_time": 3, "exit_code": 0, "real_time": 8, "test_case": "19", "output_md5": "dc16622ddc767e6bc1200fe5df2fbdfb"}, {"error": 0, "memory": 3969024, "output": null, "result": 0, "signal": 0, "cpu_time": 7, "exit_code": 0, "real_time": 8, "test_case": "20", "output_md5": "90aef91f0d9e7c3be322bd7bae41617d"}, {"error": 0, "memory": 3940352, "output": null, "result": 0, "signal": 0, "cpu_time": 6, "exit_code": 0, "real_time": 7, "test_case": "21", "output_md5": "a36e841c5230a79c2102036d2e259848"}, {"error": 0, "memory": 15282176, "output": null, "result": 0, "signal": 0, "cpu_time": 162, "exit_code": 0, "real_time": 171, "test_case": "22", "output_md5": "017335bad48f4cae20a7fb8201cc1323"}, {"error": 0, "memory": 15241216, "output": null, "result": 0, "signal": 0, "cpu_time": 166, "exit_code": 0, "real_time": 170, "test_case": "23", "output_md5": "d3eb9a9233e52948740d7eb8c3062d14"}, {"error": 0, "memory": 15212544, "output": null, "result": 0, "signal": 0, "cpu_time": 167, "exit_code": 0, "real_time": 172, "test_case": "24", "output_md5": "d1189a6e530de53bd545ae83f266820c"}, {"error": 0, "memory": 15323136, "output": null, "result": 0, "signal": 0, "cpu_time": 140, "exit_code": 0, "real_time": 140, "test_case": "25", "output_md5": "d3eb9a9233e52948740d7eb8c3062d14"}, {"error": 0, "memory": 15228928, "output": null, "result": 0, "signal": 0, "cpu_time": 165, "exit_code": 0, "real_time": 166, "test_case": "26", "output_md5": "8ecdbbf4ca2a3715337c02cb8d2ea4cc"}, {"error": 0, "memory": 15208448, "output": null, "result": 0, "signal": 0, "cpu_time": 169, "exit_code": 0, "real_time": 173, "test_case": "27", "output_md5": "a0e26081e098a15167d39b7194c5e467"}, {"error": 0, "memory": 15245312, "output": null, "result": 0, "signal": 0, "cpu_time": 143, "exit_code": 0, "real_time": 144, "test_case": "28", "output_md5": "d3eb9a9233e52948740d7eb8c3062d14"}, {"error": 0, "memory": 15224832, "output": null, "result": 0, "signal": 0, "cpu_time": 191, "exit_code": 0, "real_time": 196, "test_case": "29", "output_md5": "2b4226dd7ed6eb2d419b881f3ae9c97c"}, {"error": 0, "memory": 15216640, "output": null, "result": 0, "signal": 0, "cpu_time": 174, "exit_code": 0, "real_time": 174, "test_case": "30", "output_md5": "a195e29a87f723b4f0dc559794e86038"}, {"error": 0, "memory": 15351808, "output": null, "result": 0, "signal": 0, "cpu_time": 134, "exit_code": 0, "real_time": 139, "test_case": "31", "output_md5": "d3eb9a9233e52948740d7eb8c3062d14"}]}	C++	f	{"time_cost": 191, "memory_cost": 15351808}	root	116.34.23.161
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public."user" (id, password, last_login, username, email, create_time, admin_type, reset_password_token, reset_password_token_expire_time, auth_token, two_factor_auth, tfa_token, open_api, open_api_appkey, is_disabled, problem_permission, session_keys) FROM stdin;
2	pbkdf2_sha256$120000$AsPyyi8S9j4w$zCnLieKVpc8NhkesjUg2BQKFvDe3yv9rcbsGODXX1rE=	2020-12-17 12:02:45.066897+00	장민	guftkcldh@naver.com	2020-12-17 12:02:19.594605+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["zabdbz3i8yp8ol7bx4oawlk57uskcnle"]
22	pbkdf2_sha256$120000$zoN23dYrj3my$qLoBnOBH6D3V5wfxtkBJEvU7TRQf8bIc1wNiQ6iaPvc=	2020-12-31 09:00:01.893769+00	2018311406	ksmin1114@g.skku.edu	2020-12-31 08:59:51.180893+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["h5ic3935strjxww7y7sm428n5rok90sx"]
13	pbkdf2_sha256$120000$r3xcAT0zZJ8d$/mOtwYLh2bINIhmMSPj2jCe3Ty+lZ7VgzPgNbNOeITM=	2020-12-31 08:39:45.342913+00	2017313120	onow7353@gmail.com	2020-12-31 08:39:32.777395+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["kchexmzn7bnzf8yzonrqu5iz604vh2oz"]
20	pbkdf2_sha256$120000$VJv8xfpZxxbt$WjqfhAYC7cAU1xbkIKnPiUAgVdmIRZmhbCSgfWIks+Q=	2020-12-31 08:58:33.087458+00	2018312058	kangdyu99@gmail.com	2020-12-31 08:58:27.542393+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["50xx5m1bh55qvam5iaiyr93dnmkupbtp"]
18	pbkdf2_sha256$120000$GK1i30flFfRD$5gp99oHYtPsdS/KMJ3ozQ7xTq6DdJLZwqfZXxLZpsY0=	2020-12-31 08:49:09.529289+00	2016312332	hojoon0205@gmail.com	2020-12-31 08:48:51.971178+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["961yuxp83a33vfckru6s051bhqhazzwg"]
12	pbkdf2_sha256$120000$nIG2Kuockk9c$FWUVeNleybqUE3B1CdO3gpUBHl7WsUX8sFf2RVQamyM=	2020-12-31 08:40:07.065544+00	2016311327	ploteen@g.skku.edu	2020-12-31 08:39:31.59764+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["9v800kp9byhylowlbwfoc28ez2zra52k"]
4	pbkdf2_sha256$120000$PGXCKYaTTMi2$AcmQy83f6eFVEm9MGHzrHjltlPVBlh5IY+675B60GVQ=	2020-12-31 08:23:51.662683+00	2020311460	wannapaymoney11@gmail.com	2020-12-31 08:23:39.222362+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["vzaviwrx5zqgh07xh0vw4opcot8v0wh8"]
6	pbkdf2_sha256$120000$gthHQhsX3hsK$+omhjgtiH0YS7URO9UW49b+RhLHL9LUVE8vKlDJ3zVk=	2020-12-31 08:33:45.319368+00	cho seong hyeon	sc4259@naver.com	2020-12-31 08:30:30.377418+00	Regular User	\N	\N	\N	f	d83c2cf9fe11d17ec6f92b3ea9412d47	f	\N	f	None	["6zktdl1k875l2popldjuxe4zazerfhmk", "4k1l8ozcq9b35xnw78o106m3v4ze56m9", "irj8y4mg94gtrc4u62dgv0dj0sgautey"]
8	pbkdf2_sha256$120000$huJERu82mivj$F4dOj5z+FFMkrHEaxPFKV16z50rX/76KCMx+rsnwMRM=	2020-12-31 08:32:43.55389+00	2019311680	threedalpeng@gmail.com	2020-12-31 08:32:34.317512+00	Regular User	\N	\N	\N	f	68aeb4a7ff3d4b373f588e785613db26	f	\N	f	None	["z36etngxwapl59vudfvqc65hlg2f6x04"]
7	pbkdf2_sha256$120000$4oUkbyEzqff9$eSe6ZNrI1ChXBhVccVIOJkwWmtmZlSiVSYnf/cw1EJc=	2020-12-31 08:30:44.350074+00	2015318907	uniqueimaginate@gmail.com	2020-12-31 08:30:31.58174+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["s1uvq5ag4a7xgh21dwsprxvc3q8re6vf"]
14	pbkdf2_sha256$120000$2P96cndGIqg2$N7rF/YW+62VeNm4ajLbna+2jSos2tZWidsTA0H2JYmg=	2020-12-31 08:42:52.092555+00	2015313016	ian.lee.dev@gmail.com	2020-12-31 08:42:41.087954+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["6u8b1ytgtpjfsbaxr4vu8ox070qep8sp"]
5	pbkdf2_sha256$120000$33j4ezug3Hha$pRnAZ9CE5porMwxyejEtShrwaPtqSRh7dIC0LT48Xs8=	2020-12-31 08:31:07.824238+00	dalpengx3	dalpengx3@g.skku.edu	2020-12-31 08:29:51.655351+00	Regular User	\N	\N	\N	f	73c0e5940067f6a56833713316a461a1	f	\N	f	None	["p2e4gz7a1uqgqhg2b4uak5hmqg759til"]
9	pbkdf2_sha256$120000$wTxJUhLwvBbL$3Bx/WFbBMyOnOWeVukohAw8OBE9jWs6GPvb/Bfg7afg=	2020-12-31 08:34:59.90837+00	jinsuby	wlstjq0602@naver.com	2020-12-31 08:34:49.898062+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["a0l17gdhwl3pp34vmct9hgqoykykkght"]
3	pbkdf2_sha256$120000$k1k1qihf5hL6$aFGGFd2dZTWDMt7x+xGg65KMfCQ9Whh+YstpO0tYUWc=	2020-12-29 05:51:11.642433+00	test	test@gmail.com	2020-12-29 05:51:03.134788+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["e1ysnkl0fukdljyf2hpjhwmksf9ixkvz"]
10	pbkdf2_sha256$120000$Flcjd0jBYVeO$MuTwi32xatmlL3qedRiXQZI2e4XvG06FB6vUtd5W58E=	2020-12-31 08:35:03.10814+00	2020311119	st42597@gmail.com	2020-12-31 08:34:55.822173+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["5ronyxug4vtn0x3ty946z4rew8ou8cyt"]
19	pbkdf2_sha256$120000$CiWhp5ZNvAfT$on0FZcKCvuaxJhaFH0cfy0/9Kil+rLk9e/YAVvGme/g=	2021-01-02 12:56:25.584324+00	2016310249	adornt01@naver.com	2020-12-31 08:52:44.480384+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["ex2iv3k49vaedgep7mti6lu329j1grql", "lg4xbyk7bxk6jlrmhc9v1jzfdyggx36m", "ksgbs02nydj7llcu3ftyddy1qv61c5t8", "ipazlfs22y5h8e3hmifvumrx0b2evqyq", "v074gx3dfih6l22d4xincyyuem29uwn5"]
15	pbkdf2_sha256$120000$lw7FjQA5FPGy$w4zd/wzl+kUt7/43r/H4D6g6ui4zXDANvO3dGSS62Xw=	2020-12-31 08:43:24.593823+00	2017311706	vbnmzx1@skku.edu	2020-12-31 08:43:10.953878+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["fzgjv2b1mex7sqkm5q4q54bwf5eaqceo"]
11	pbkdf2_sha256$120000$6LaS2p11v6GC$TWCUw8ZfWgjXOtOB2H9T+sYY2XZQIaNz5hGBDuC0aco=	2020-12-31 08:36:07.03975+00	2017311005	zxc91911003@gmail.com	2020-12-31 08:35:49.795336+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["n8tlrx9jpdwu9qo8dgivi6sht1irv9lu"]
21	pbkdf2_sha256$120000$32kQ9EzmTYpR$lsVGLSMjlJs00F/DFttlKwR3MTyfX3mXQ8qRYZwh0eg=	2020-12-31 08:59:00.868045+00	2020310781	fkddl1436@naver.com	2020-12-31 08:58:49.093816+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["2erj6u6l6lnb4uokoc3smhg6dgdndjx9"]
16	pbkdf2_sha256$120000$cp80yUUvaJuV$9Od6mdjXropRuugLBnhKIgn0YzRBEdgMgrZlkUb8yTg=	2020-12-31 08:43:55.04658+00	2020314959	jony2000@g.skku.edu	2020-12-31 08:43:47.461022+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["wcv98dk5h4tlyzik67udmtvzkayhxtjh"]
17	pbkdf2_sha256$120000$MvcKpRz0gozZ$J9VEqs2KtuDTjnw8JrIh/+h39VQGcE/hNv+O78uXjIo=	2020-12-31 08:44:32.092096+00	2019311277	baksa1849@g.skku.edu	2020-12-31 08:44:26.410957+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["vodf0te4eqkdxgirlvd8g9yxdbyk2mlp"]
24	pbkdf2_sha256$120000$xpeSsIx8bqHj$dNYiGKkQca4EPctUaU2n8UQowSlqksaC1ujGO/xGIgI=	2020-12-31 09:22:55.019215+00	2017312475	seryeong971120@gmail.com	2020-12-31 09:22:43.747319+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["4gld7rjui77rt88cws0hb9fgnx78t0aa"]
23	pbkdf2_sha256$120000$iM0INljabZmW$PzgeN26NgAfmdeTzJbb3IaLek9fPs4qDoiLlVMFGdpE=	2020-12-31 09:11:48.465738+00	2016312057	timeslump@naver.com	2020-12-31 09:11:43.269521+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["2xxictyn39hyl2co0g89cbu42e71ggfx"]
25	pbkdf2_sha256$120000$teN1NozB3CXI$eGzSU2bjuO0oVbU8JMGGBnhnwHUM11M4SDr3Sbv5fgo=	2020-12-31 09:45:21.400762+00	2020313223	sjk1117@g.skku.edu	2020-12-31 09:45:09.359692+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["rvpbgq3jxhzfs7ljc5cmvu1950kju8mt"]
26	pbkdf2_sha256$120000$Sr2O2fncM3Ck$PEyFKI32XRNhswi/PPUcqJN11nwI4v73Ottp4Tj1sC4=	2020-12-31 09:47:32.739064+00	2016311072	shjohw12@skku.edu	2020-12-31 09:47:24.114996+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["5uasz1yvxzgrylslhwx90rfqfr96nj5n"]
27	pbkdf2_sha256$120000$GRyh92fhIHgN$bAkJE8TsGlAqp6kRNuXzINm12tIMYYGqrxiR1y1osFs=	2020-12-31 10:10:22.654504+00	2016312924	brianjune@naver.com	2020-12-31 10:09:53.856497+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["t3o2kqk4qhmyhqw85tbq4eeki2w5x52i"]
28	pbkdf2_sha256$120000$WMqy7sKySLEg$XTZlB3RjmDKWDWcwS9IApQ1mmSpbcHv2fHBfkFUsOjM=	2020-12-31 10:48:06.21283+00	2019310631	onsaemiro@g.skku.edu	2020-12-31 10:42:09.695666+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["met6kun7bjas6o309i88cs3812irt2v4", "t5xgqk0dvtyj781dfedho7vt86abzdpy", "mdztr08wyhbo3tfwucwkf1obc0evcyr2"]
29	pbkdf2_sha256$120000$1LxKahqmR6Gj$1grhYdkN0t32yc+Oz8lMUxqWrMYRwMW9Dx0mWq77CB4=	2020-12-31 14:01:55.147175+00	2019312978	2000daehee@naver.com	2020-12-31 14:01:41.229547+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["eos79n1p529hxxyj5lrckphc5wxtmiep"]
30	pbkdf2_sha256$120000$41UqFLYw93F4$W7EzNmiFA7wuQ8uDfiGX8JTHv3s/RYnkvTqhoaGrwJc=	2020-12-31 14:43:42.987868+00	2019313416	alsgh0986@gmail.com	2020-12-31 14:43:33.390679+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["gkzia1n4gvbrnle5fr3yrfw0s36qgigp"]
31	pbkdf2_sha256$120000$ElknxpmxVtf9$iJrNUVJYrrct/t8t5fSUIYEeelxeNvaoCcbHVYFKdsM=	2020-12-31 15:26:20.115792+00	2014311827	zxcvbnm096@g.skku.edu	2020-12-31 15:26:11.166427+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["pnros3i0le5mor0b3uee443cyk5ngv4f"]
41	pbkdf2_sha256$120000$H3OqWfbK06bt$0y/KasN+7IOgxtZcJW4BOQymYHSDsXhORX84Qt7LBk0=	2021-01-02 13:27:40.326411+00	2015312805	kjh105702@g.skku.edu	2021-01-02 13:26:59.177449+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["9z1k2kzd1j6lzansuj5c0rvplir7fs25"]
32	pbkdf2_sha256$120000$MwEixzslglYA$6JIItUjLM+dXA/ZF3fWefsEt1f5ppDz8N2wfFdoydsA=	2020-12-31 20:37:10.761329+00	2020312218	ankim0725@gmail.com	2020-12-31 20:35:56.831344+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["ko2mviayby5wtsvz2br0n05guj61g0ra"]
1	pbkdf2_sha256$120000$e2ABV9xQ5DYo$rv4H6Zp4vyJObIOuQ8GNh3J+ivYyFUPOF4/BVu/IHAM=	2021-01-02 07:27:38.843774+00	root	\N	2020-12-17 08:13:42.278834+00	Super Admin	\N	\N	\N	f	\N	f	\N	f	All	["wdlabiagypco1er81u0hx1llukovpyla", "pghvlhtjsaebcaank5lyuez4ohwe26wl", "xjtg1r0ya34tb5n1bqrd79aals3eizou", "bpw1tqbvwudigzl4wjvz39s9v3c23mqt", "ra6h0u4cq3738fjbrjktql3fx4vktf35", "cffxf8ptb80edupi0lspelns0sqizt5q"]
33	pbkdf2_sha256$120000$IO62zzAHBHdl$+XdItoqvhuFp+Nj2U7mKcKB+oQyx3kv2AheLW1QCVSI=	2020-12-31 23:59:35.527278+00	2015313375	bestowing02@gmail.com	2020-12-31 23:59:25.298723+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["6wsrbbqb1pb5hc5ke17knd8w0wzlztxd"]
37	pbkdf2_sha256$120000$ENp5ymIszEqU$nFijLkomOp8QJIK771C/v1rsjsq6+SJQ1xX6mD9WXCk=	\N	전대영	jdy2995@naver.com	2021-01-02 08:10:47.333517+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	[]
34	pbkdf2_sha256$120000$Cc5i6tUpwzvX$QLqGqYKbp4mgD+LmRIcn3kFdyQ+SW6FzGvRyUtS9q6s=	2021-01-01 06:41:22.500591+00	장이준	jangij0824@gmail.com	2021-01-01 06:41:10.303985+00	Regular User	\N	\N	\N	f	97a9e662fd66847316e5d64927849ede	f	\N	f	None	["bs2bbhon67knn1gjnn9xs3kihv2ap0aq"]
35	pbkdf2_sha256$120000$DMRGnyLEnHfw$BBZL+QWybwR1Q/oLgxyU4Dpf7Ui4AUu56KkysqAvMUk=	2021-01-01 06:46:05.515306+00	2019313491	ijun0824@naver.com	2021-01-01 06:45:53.248564+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["o4m0f8m1yw0eoxi5g9qvv5tsfgqck3i8"]
38	pbkdf2_sha256$120000$AWvBtDcOxUjW$0cBxhoKFcvlO5me7+5OEA+rWiSagE+WZ8MgwtVDF1Yw=	2021-01-02 09:05:37.634+00	서경태	tjrudxo0124@naver.com	2021-01-02 09:05:29.41692+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["pu1mekgju6stwy5nlmtspvyf6jhi9x86"]
39	pbkdf2_sha256$120000$mNy6LxWi4XdC$u6ilVfDp0Vzn2x9pb+vBrzuGbEWPkrpZwv6kblAoUaA=	2021-01-02 12:07:02.116031+00	2019312342	leees2000@gmail.com	2021-01-02 12:06:18.878116+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["p3ynyoionwb7sb7iyvsqk6jhhu35egj8"]
36	pbkdf2_sha256$120000$tXnyPRzkH5BS$PxESQ5C+aeOF8UUQw6JRDwI8C6Yu29RFHpxncwc8iuc=	2021-01-01 18:00:27.955735+00	2017313109	dlwnsxo98@naver.com	2021-01-01 18:00:14.863724+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["xcoljbir9836gbjpdvwduirkz9x2mclq"]
40	pbkdf2_sha256$120000$N3fQEhNHVkRf$9DHa5n/eO9cTT4APVsyhIv/t62d4eb+zdymedanv1jk=	2021-01-02 12:46:40.694354+00	2019314992	1dotolee@gmail.com	2021-01-02 12:46:23.71419+00	Regular User	\N	\N	\N	f	\N	f	\N	f	None	["ehm5kqr1c4kh8h9g8iihxkvtak94efsw"]
\.


--
-- Data for Name: user_profile; Type: TABLE DATA; Schema: public; Owner: onlinejudge
--

COPY public.user_profile (id, acm_problems_status, avatar, blog, mood, accepted_number, submission_number, github, school, major, user_id, total_score, oi_problems_status, real_name, language) FROM stdin;
32	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	32	0	{}	\N	\N
33	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	33	0	{}	\N	\N
34	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	34	0	{}	2019313491	\N
35	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	35	0	{}	\N	\N
36	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	36	0	{}	\N	\N
37	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	37	0	{}	\N	\N
38	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	38	0	{}	\N	\N
39	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	39	0	{}	\N	\N
40	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	40	0	{}	최재민	\N
41	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	41	0	{}	\N	\N
2	{"problems": {"4": {"_id": "A", "status": -1}}}	/public/avatar/default.png	\N	\N	0	2	\N	\N	\N	2	0	{}	\N	\N
1	{"problems": {"1": {"_id": "1", "status": -2}, "2": {"_id": "2", "status": 0}, "4": {"_id": "A", "status": 0}, "5": {"_id": "2", "status": 0}}}	/public/avatar/default.png	\N	\N	3	18	\N	\N	\N	1	0	{}	\N	\N
3	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	3	0	{}	\N	\N
4	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	4	0	{}	\N	\N
5	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	5	0	{}	\N	\N
6	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	6	0	{}	\N	\N
7	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	7	0	{}	\N	\N
8	{}	/public/avatar/default.png	\N	\N	0	0	\N	소프트웨어대학	소프트웨어학과	8	0	{}	김정원	en-US
9	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	9	0	{}	\N	\N
10	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	10	0	{}	\N	\N
11	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	11	0	{}	\N	\N
12	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	12	0	{}	\N	\N
13	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	13	0	{}	\N	\N
14	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	14	0	{}	\N	\N
15	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	15	0	{}	\N	\N
16	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	16	0	{}	\N	\N
17	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	17	0	{}	\N	\N
18	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	18	0	{}	\N	\N
19	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	19	0	{}	\N	\N
20	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	20	0	{}	\N	\N
21	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	21	0	{}	\N	\N
22	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	22	0	{}	\N	\N
23	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	23	0	{}	\N	\N
24	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	24	0	{}	\N	\N
25	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	25	0	{}	\N	\N
26	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	26	0	{}	\N	\N
27	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	27	0	{}	\N	\N
28	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	28	0	{}	\N	\N
29	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	29	0	{}	\N	\N
30	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	30	0	{}	\N	\N
31	{}	/public/avatar/default.png	\N	\N	0	0	\N	\N	\N	31	0	{}	\N	\N
\.


--
-- Name: acm_contest_rank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.acm_contest_rank_id_seq', 1, false);


--
-- Name: announcement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.announcement_id_seq', 3, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 68, true);


--
-- Name: contest_announcement_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.contest_announcement_id_seq', 1, false);


--
-- Name: contest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.contest_id_seq', 2, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 17, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 65, true);


--
-- Name: judge_server_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.judge_server_id_seq', 2, true);


--
-- Name: oi_contest_rank_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.oi_contest_rank_id_seq', 1, false);


--
-- Name: options_sysoptions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.options_sysoptions_id_seq', 10, true);


--
-- Name: problem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.problem_id_seq', 20, true);


--
-- Name: problem_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.problem_tag_id_seq', 6, true);


--
-- Name: problem_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.problem_tags_id_seq', 45, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.user_id_seq', 41, true);


--
-- Name: user_profile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: onlinejudge
--

SELECT pg_catalog.setval('public.user_profile_id_seq', 41, true);


--
-- Name: acm_contest_rank acm_contest_rank_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.acm_contest_rank
    ADD CONSTRAINT acm_contest_rank_pkey PRIMARY KEY (id);


--
-- Name: acm_contest_rank acm_contest_rank_user_id_contest_id_26151d10_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.acm_contest_rank
    ADD CONSTRAINT acm_contest_rank_user_id_contest_id_26151d10_uniq UNIQUE (user_id, contest_id);


--
-- Name: announcement announcement_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.announcement
    ADD CONSTRAINT announcement_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: contest_announcement contest_announcement_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest_announcement
    ADD CONSTRAINT contest_announcement_pkey PRIMARY KEY (id);


--
-- Name: contest contest_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest
    ADD CONSTRAINT contest_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_dramatiq_task django_dramatiq_task_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_dramatiq_task
    ADD CONSTRAINT django_dramatiq_task_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: judge_server judge_server_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.judge_server
    ADD CONSTRAINT judge_server_pkey PRIMARY KEY (id);


--
-- Name: oi_contest_rank oi_contest_rank_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.oi_contest_rank
    ADD CONSTRAINT oi_contest_rank_pkey PRIMARY KEY (id);


--
-- Name: oi_contest_rank oi_contest_rank_user_id_contest_id_fe51a302_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.oi_contest_rank
    ADD CONSTRAINT oi_contest_rank_user_id_contest_id_fe51a302_uniq UNIQUE (user_id, contest_id);


--
-- Name: options_sysoptions options_sysoptions_key_key; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.options_sysoptions
    ADD CONSTRAINT options_sysoptions_key_key UNIQUE (key);


--
-- Name: options_sysoptions options_sysoptions_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.options_sysoptions
    ADD CONSTRAINT options_sysoptions_pkey PRIMARY KEY (id);


--
-- Name: problem problem__id_contest_id_346645fe_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem
    ADD CONSTRAINT problem__id_contest_id_346645fe_uniq UNIQUE (_id, contest_id);


--
-- Name: problem problem_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem
    ADD CONSTRAINT problem_pkey PRIMARY KEY (id);


--
-- Name: problem_tag problem_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tag
    ADD CONSTRAINT problem_tag_pkey PRIMARY KEY (id);


--
-- Name: problem_tags problem_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_pkey PRIMARY KEY (id);


--
-- Name: problem_tags problem_tags_problem_id_problemtag_id_318459d1_uniq; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_problem_id_problemtag_id_318459d1_uniq UNIQUE (problem_id, problemtag_id);


--
-- Name: submission submission_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_profile user_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_pkey PRIMARY KEY (id);


--
-- Name: user_profile user_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_user_id_key UNIQUE (user_id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: acm_contest_rank_contest_id_21030ccd; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX acm_contest_rank_contest_id_21030ccd ON public.acm_contest_rank USING btree (contest_id);


--
-- Name: acm_contest_rank_user_id_40391ab2; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX acm_contest_rank_user_id_40391ab2 ON public.acm_contest_rank USING btree (user_id);


--
-- Name: announcement_created_by_id_359ccf50; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX announcement_created_by_id_359ccf50 ON public.announcement USING btree (created_by_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: contest_announcement_contest_id_a8cb419f; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX contest_announcement_contest_id_a8cb419f ON public.contest_announcement USING btree (contest_id);


--
-- Name: contest_announcement_created_by_id_469a14ce; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX contest_announcement_created_by_id_469a14ce ON public.contest_announcement USING btree (created_by_id);


--
-- Name: contest_created_by_id_a763ca7e; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX contest_created_by_id_a763ca7e ON public.contest USING btree (created_by_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: oi_contest_rank_contest_id_171fcdaf; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX oi_contest_rank_contest_id_171fcdaf ON public.oi_contest_rank USING btree (contest_id);


--
-- Name: oi_contest_rank_user_id_0ba36852; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX oi_contest_rank_user_id_0ba36852 ON public.oi_contest_rank USING btree (user_id);


--
-- Name: problem__id_919b1d80; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX problem__id_919b1d80 ON public.problem USING btree (_id);


--
-- Name: problem_contest_id_328e013a; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX problem_contest_id_328e013a ON public.problem USING btree (contest_id);


--
-- Name: problem_created_by_id_cb362143; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX problem_created_by_id_cb362143 ON public.problem USING btree (created_by_id);


--
-- Name: problem_tags_problem_id_866ecb8d; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX problem_tags_problem_id_866ecb8d ON public.problem_tags USING btree (problem_id);


--
-- Name: problem_tags_problemtag_id_72d20571; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX problem_tags_problemtag_id_72d20571 ON public.problem_tags USING btree (problemtag_id);


--
-- Name: submission_contest_id_775716d5; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX submission_contest_id_775716d5 ON public.submission USING btree (contest_id);


--
-- Name: submission_problem_id_76847b55; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX submission_problem_id_76847b55 ON public.submission USING btree (problem_id);


--
-- Name: submission_result_37e2f67a; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX submission_result_37e2f67a ON public.submission USING btree (result);


--
-- Name: submission_user_id_3779a8c1; Type: INDEX; Schema: public; Owner: onlinejudge
--

CREATE INDEX submission_user_id_3779a8c1 ON public.submission USING btree (user_id);


--
-- Name: acm_contest_rank acm_contest_rank_contest_id_21030ccd_fk_contest_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.acm_contest_rank
    ADD CONSTRAINT acm_contest_rank_contest_id_21030ccd_fk_contest_id FOREIGN KEY (contest_id) REFERENCES public.contest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: acm_contest_rank acm_contest_rank_user_id_40391ab2_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.acm_contest_rank
    ADD CONSTRAINT acm_contest_rank_user_id_40391ab2_fk_user_id FOREIGN KEY (user_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: announcement announcement_created_by_id_359ccf50_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.announcement
    ADD CONSTRAINT announcement_created_by_id_359ccf50_fk_user_id FOREIGN KEY (created_by_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contest_announcement contest_announcement_contest_id_a8cb419f_fk_contest_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest_announcement
    ADD CONSTRAINT contest_announcement_contest_id_a8cb419f_fk_contest_id FOREIGN KEY (contest_id) REFERENCES public.contest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contest_announcement contest_announcement_created_by_id_469a14ce_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest_announcement
    ADD CONSTRAINT contest_announcement_created_by_id_469a14ce_fk_user_id FOREIGN KEY (created_by_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: contest contest_created_by_id_a763ca7e_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.contest
    ADD CONSTRAINT contest_created_by_id_a763ca7e_fk_user_id FOREIGN KEY (created_by_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oi_contest_rank oi_contest_rank_contest_id_171fcdaf_fk_contest_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.oi_contest_rank
    ADD CONSTRAINT oi_contest_rank_contest_id_171fcdaf_fk_contest_id FOREIGN KEY (contest_id) REFERENCES public.contest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oi_contest_rank oi_contest_rank_user_id_0ba36852_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.oi_contest_rank
    ADD CONSTRAINT oi_contest_rank_user_id_0ba36852_fk_user_id FOREIGN KEY (user_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: problem problem_contest_id_328e013a_fk_contest_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem
    ADD CONSTRAINT problem_contest_id_328e013a_fk_contest_id FOREIGN KEY (contest_id) REFERENCES public.contest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: problem problem_created_by_id_cb362143_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem
    ADD CONSTRAINT problem_created_by_id_cb362143_fk_user_id FOREIGN KEY (created_by_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: problem_tags problem_tags_problem_id_866ecb8d_fk_problem_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_problem_id_866ecb8d_fk_problem_id FOREIGN KEY (problem_id) REFERENCES public.problem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: problem_tags problem_tags_problemtag_id_72d20571_fk_problem_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_problemtag_id_72d20571_fk_problem_tag_id FOREIGN KEY (problemtag_id) REFERENCES public.problem_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: submission submission_contest_id_775716d5_fk_contest_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_contest_id_775716d5_fk_contest_id FOREIGN KEY (contest_id) REFERENCES public.contest(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: submission submission_problem_id_76847b55_fk_problem_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.submission
    ADD CONSTRAINT submission_problem_id_76847b55_fk_problem_id FOREIGN KEY (problem_id) REFERENCES public.problem(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_profile user_profile_user_id_8fdce8e2_fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: onlinejudge
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_user_id_8fdce8e2_fk_user_id FOREIGN KEY (user_id) REFERENCES public."user"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15
-- Dumped by pg_dump version 10.15

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

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: onlinejudge
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15
-- Dumped by pg_dump version 10.15

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

--
-- Name: DATABASE template1; Type: COMMENT; Schema: -; Owner: onlinejudge
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

