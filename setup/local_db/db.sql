CREATE TABLE satellites(
   id serial PRIMARY KEY,
   sat_number INTEGER NOT NULL,
   sat_name TEXT NOT NULL,
   constellation TEXT,
   other_ids INTEGER ARRAY,
   date_added TIMESTAMPTZ NOT NULL,
   date_modified TIMESTAMPTZ NOT NULL,
   UNIQUE (sat_number, sat_name)
);

CREATE TABLE tle(
   id serial PRIMARY KEY,
   sat_id serial NOT NULL,
   date_collected TIMESTAMPTZ NOT NULL,
   tle_line1 TEXT NOT NULL,
   tle_line2 TEXT NOT NULL,
   epoch TIMESTAMPTZ NOT NULL,
   is_supplemental BOOLEAN NOT NULL,
   data_source TEXT NOT NULL,
   FOREIGN KEY (sat_id)
      REFERENCES satellites (id),
   UNIQUE (sat_id, epoch, data_source)
);


-- Changes: 1-11-24
ALTER TABLE public.satellites
ADD COLUMN other_ids INTEGER ARRAY;

ALTER TABLE public.satellites
ADD COLUMN date_added TIMESTAMPTZ NOT NULL DEFAULT NOW();

ALTER TABLE public.satellites
ADD COLUMN date_modified TIMESTAMPTZ NOT NULL DEFAULT NOW();

ALTER TABLE public.satellites
DROP CONSTRAINT satellites_sat_number_key;

ALTER TABLE public.satellites
ADD CONSTRAINT unique_sat UNIQUE (sat_number, sat_name);

ALTER TABLE public.tle
ADD COLUMN data_source TEXT NOT NULL DEFAULT 'celestrak';


-- Changes: 2-6-24
ALTER TABLE public.tle
DROP CONSTRAINT tle_sat_id_epoch_key;

ALTER TABLE public.tle
ADD CONSTRAINT unique_tle UNIQUE (sat_id, epoch, data_source);
