from __future__ import generators
import logging
import pprint
import psycopg2
import psycopg2.extras
import yaml
from datetime import datetime

import model


class VideoProvider (model.Provider):
    table_name = "video"

    def create (self, record):
        msg = "Inserting video record for '{0}'."
        logging.info(msg.format(record["title"]))
        record["timestamp_creation"] = datetime.now()

        with self.get_db_cursor() as cur:
            cur.execute("INSERT INTO video (id, video_id, site, title, description, thumbnail_url, timestamp_creation, timestamp_publish, description_snippet) VALUES(default, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (record["video_id"], record["site"], record["title"], record["description"], record["thumbnail_url"], record["timestamp_creation"], record["timestamp_publish"], record["snippet"],))
            record['id'] = cur.fetchone()['id']
            return Video(record)

    def exists (self, id_):
        """ Returns True if record with id exists """
        return self.read (id_) is not None

    def exists_by_video_id (self, video_id):
        """ Returns True if record with video_id exists """
        return self.read_by_video_id (video_id) is not None

    def make_model (self, props):
        return Video (props)

    def read (self, id_):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM video WHERE id = (%s)", (id_,))
            res = cur.fetchone()

            if res is not None:
                return Video (res)
            else:
                return None

    def read_by_video_id (self, video_id):
        with self.get_db_cursor() as cur:
            cur.execute("SELECT * FROM video WHERE video_id = (%s)", (video_id,))
            res = cur.fetchone()

            if res is not None:
                return Video (res)
            else:
                return None


class Video (model.Model):
    object_type = 'video'
