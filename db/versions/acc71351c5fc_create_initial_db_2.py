"""create initial db 2

Revision ID: acc71351c5fc
Revises: 
Create Date: 2018-06-30 19:37:35.274139+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'acc71351c5fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("bs12_rank",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(32), index=True, unique=True),
        sa.Column("permissions", sa.Integer),
        sa.Column("flags", sa.Integer, server_default=sa.text("0")),
    )
    op.create_table("bs12_player",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ckey", sa.String(32), index=True),
        sa.Column("first_seen", sa.DateTime, server_default=sa.func.now()),
        sa.Column("last_seen", sa.DateTime),
        sa.Column("rank", sa.Integer, sa.ForeignKey("bs12_rank.id"), nullable=True),
        sa.Column("staffwarn", sa.Text, nullable=True),
    )
    op.create_table("bs12_round",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("roundid", sa.String(16), index=True, unique=True),
        sa.Column("start", sa.DateTime, server_default=sa.func.now()),
        sa.Column("end", sa.DateTime),
    )
    op.create_table("bs12_ip",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ip", sa.Integer(32), index=True, unique=True),
    )
    op.create_table("bs12_clientid",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("clientid", sa.Integer(32), index=True, unique=True),
    )
    op.create_table("bs12_login",
        sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("player", sa.Integer, sa.ForeignKey("bs12_player.id")),
        sa.Column("ip", sa.Integer, sa.ForeignKey("bs12_ip.id")),
        sa.Column("clientid", sa.Integer, sa.ForeignKey("bs12_clientid.id")),
        sa.Column("round", sa.Integer, sa.ForeignKey("bs12_round.id")),
    )
    op.create_table("bs12_ban",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ckey", sa.String(32)),
        sa.Column("admin", sa.Integer, sa.ForeignKey("bs12_player.id")),
        sa.Column("stamp", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_table("bs12_ban_reason",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ban", sa.Integer, sa.ForeignKey("bs12_ban.id"), index=True),
        sa.Column("admin", sa.Integer, sa.ForeignKey("bs12_player.id")),
        sa.Column("stamp", sa.DateTime, server_default=sa.func.now()),
        sa.Column("reason", sa.String(256)),
    )
    op.create_table("bs12_ban_scope",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ban", sa.Integer, sa.ForeignKey("bs12_ban.id"), index=True),
        sa.Column("admin", sa.Integer, sa.ForeignKey("bs12_player.id")),
        sa.Column("stamp", sa.DateTime, server_default=sa.func.now()),
        sa.Column("scope", sa.Text),
    )
    op.create_table("bs12_ban_expiry",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("ban", sa.Integer, sa.ForeignKey("bs12_ban.id"), index=True),
        sa.Column("admin", sa.Integer, sa.ForeignKey("bs12_player.id")),
        sa.Column("stamp", sa.DateTime, server_default=sa.func.now()),
        sa.Column("expiration", sa.DateTime, nullable=True),
    )

    op.execute("""CREATE OR REPLACE VIEW bs12_active_ban_reason AS
                  SELECT id, ban, reason FROM bs12_ban_reason
                  WHERE id IN (SELECT MAX(id) AS id FROM bs12_ban_reason GROUP BY ban);""")

    op.execute("""CREATE OR REPLACE VIEW bs12_active_ban_scope AS
                  SELECT id, ban, scope FROM bs12_ban_scope
                  WHERE id IN (SELECT MAX(id) AS id FROM bs12_ban_scope GROUP BY ban);""")

    op.execute("""CREATE OR REPLACE VIEW bs12_active_ban_expiry AS
                  SELECT id, ban, expiration FROM bs12_ban_expiry
                  WHERE id IN (SELECT MAX(id) AS id FROM bs12_ban_expiry GROUP BY ban);""")

    op.execute("""CREATE OR REPLACE VIEW bs12_active_ban AS
                  SELECT bs12_ban.id, bs12_ban.ckey, bs12_ban.admin, reason, scope, expiration
                  FROM bs12_ban
                  INNER JOIN bs12_active_ban_reason AS r ON bs12_ban.id = r.ban
                  INNER JOIN bs12_active_ban_scope AS s ON bs12_ban.id = s.ban
                  INNER JOIN bs12_active_ban_expiry AS e ON bs12_ban.id = e.ban
                  WHERE expiration > NOW() OR expiration IS NULL;""")

def downgrade():
    op.execute("DROP VIEW bs12_active_ban;")
    op.execute("DROP VIEW bs12_active_ban_expiry;")
    op.execute("DROP VIEW bs12_active_ban_scope;")
    op.execute("DROP VIEW bs12_active_ban_reason;")
    
    op.drop_table("bs12_ban_expiry")
    op.drop_table("bs12_ban_scope")
    op.drop_table("bs12_ban_reason")
    op.drop_table("bs12_ban")
    op.drop_table("bs12_login")
    op.drop_table("bs12_clientid")
    op.drop_table("bs12_ip")
    op.drop_table("bs12_round")
    op.drop_table("bs12_player")
    op.drop_table("bs12_rank")
