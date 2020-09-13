"""Add metrics table

Revision ID: b89903c683c5
Revises: 16b5e0d25426
Create Date: 2020-09-13 19:19:49.684092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b89903c683c5"
down_revision = "16b5e0d25426"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "metrics",
        sa.Column("zipcode_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.Integer(), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.Column("num_sensors", sa.Integer(), nullable=False),
        sa.Column("max_sensor_distance", sa.Float(), nullable=False),
        sa.Column("min_sensor_distance", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["zipcode_id"], ["zipcodes.id"], name="metrics_zipcodes_fkey"
        ),
        sa.PrimaryKeyConstraint("zipcode_id", "timestamp"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("metrics")
    # ### end Alembic commands ###