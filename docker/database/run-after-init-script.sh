#!/usr/bin/env bash

set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
DO \$\$
BEGIN
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='wagtailcore_site') THEN
    UPDATE wagtailcore_site SET
      hostname = '${WAGTAIL_SITE_HOSTNAME-localhost}',
      port = '${WAGTAIL_SITE_PORT-80}',
      site_name = '${WAGTAIL_SITE_NAME-Dev}'
    WHERE is_default_site = TRUE;
  END IF;
  IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name='auth_user') THEN
    UPDATE auth_user SET
      password = '${WAGTAIL_USER_PASSWORD-pbkdf2_sha256\$36000\$Q6T4uYTWfQnP\$pErPo1iWfTDAHTRZxC+aboPjo3NzIrR0Ks9x521APAg=}';
  END IF;
END
\$\$;
EOSQL
