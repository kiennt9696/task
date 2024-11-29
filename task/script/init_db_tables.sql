-- Database: task_management

DROP DATABASE IF EXISTS task_management;

CREATE DATABASE task_management
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'English_United States.1252'
    LC_CTYPE = 'English_United States.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Init table

BEGIN;

CREATE TABLE IF NOT EXISTS public.task
(
    id character varying COLLATE pg_catalog."default" NOT NULL,
    title character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    creator character varying COLLATE pg_catalog."default",
    parent_id character varying COLLATE pg_catalog."default",
    type_id integer,
    status_id integer,
    severity_id integer,
    assignee character varying COLLATE pg_catalog."default",
    due_date timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    updated_by character varying COLLATE pg_catalog."default",
    CONSTRAINT task_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.task_severity
(
    id serial NOT NULL,
    name character varying COLLATE pg_catalog."default",
    CONSTRAINT task_severity_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.task_status
(
    id serial NOT NULL,
    name character varying COLLATE pg_catalog."default",
    CONSTRAINT task_status_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.transition
(
    id serial NOT NULL,
    name character varying COLLATE pg_catalog."default",
    from_status_id integer,
    to_status_id integer,
    workflow_id integer,
    resolution character varying COLLATE pg_catalog."default",
    comment text COLLATE pg_catalog."default",
    requires_approval boolean,
    approver character varying COLLATE pg_catalog."default",
    CONSTRAINT transition_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.workflow
(
    id serial NOT NULL,
    name character varying COLLATE pg_catalog."default",
    description character varying COLLATE pg_catalog."default",
    CONSTRAINT workflow_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.task_type
(
    id serial NOT NULL,
    name character varying COLLATE pg_catalog."default",
    workflow_id integer,
    CONSTRAINT task_type_pkey PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.task
    ADD CONSTRAINT task_parent_id_fkey FOREIGN KEY (parent_id)
    REFERENCES public.task (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.task
    ADD CONSTRAINT task_severity_id_fkey FOREIGN KEY (severity_id)
    REFERENCES public.task_severity (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.task
    ADD CONSTRAINT task_status_id_fkey FOREIGN KEY (status_id)
    REFERENCES public.task_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.task
    ADD CONSTRAINT task_type_id_fkey FOREIGN KEY (type_id)
    REFERENCES public.task_type (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.transition
    ADD CONSTRAINT transition_from_status_id_fkey FOREIGN KEY (from_status_id)
    REFERENCES public.task_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.transition
    ADD CONSTRAINT transition_to_status_id_fkey FOREIGN KEY (to_status_id)
    REFERENCES public.task_status (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.transition
    ADD CONSTRAINT transition_workflow_id_fkey FOREIGN KEY (workflow_id)
    REFERENCES public.workflow (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;


ALTER TABLE IF EXISTS public.task_type
    ADD CONSTRAINT task_type_workflow_id_fkey FOREIGN KEY (workflow_id)
    REFERENCES public.workflow (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;