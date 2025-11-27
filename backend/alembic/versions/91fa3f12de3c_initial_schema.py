"""Initial schema."""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from alembic import op

revision = "91fa3f12de3c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    motion_classification_enum = postgresql.ENUM(
        "substantive",
        "subsidiary",
        "privileged",
        "incidental",
        name="motionclassification",
        create_type=False,
    )
    vote_choice_enum = postgresql.ENUM(
        "yea",
        "nay",
        "abstain",
        name="votechoice",
        create_type=False,
    )

    motion_classification_enum.create(op.get_bind(), checkfirst=True)
    vote_choice_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "mps",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("riding", sa.String(), nullable=False),
        sa.Column("party", sa.String(), nullable=False),
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("attendance_rate", sa.Float(), nullable=True),
        sa.Column("party_line_voting_rate", sa.Float(), nullable=True),
        sa.Column("years_in_office", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_mps_id", "mps", ["id"])

    op.create_table(
        "motions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("introduced_by_mp_id", sa.Integer(), nullable=False),
        sa.Column("introduced_by_party", sa.String(), nullable=True),
        sa.Column("vote_results_by_party", sa.JSON(), nullable=True),
        sa.Column("passed", sa.Boolean(), nullable=True),
        sa.Column("categories", sa.ARRAY(sa.String()), nullable=True),
        sa.Column(
            "classification",
            motion_classification_enum,
            nullable=False,
        ),
        sa.Column("date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["introduced_by_mp_id"], ["mps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_motions_id", "motions", ["id"])

    op.create_table(
        "speeches",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mp_id", sa.Integer(), nullable=False),
        sa.Column("motion_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["mp_id"], ["mps.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["motion_id"], ["motions.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_speeches_id", "speeches", ["id"])

    op.create_table(
        "spending_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mp_id", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("fiscal_year", sa.String(), nullable=False),
        sa.Column("details_url", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["mp_id"], ["mps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_spending_entries_id", "spending_entries", ["id"])

    op.create_table(
        "transparency_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mp_id", sa.Integer(), nullable=False),
        sa.Column("registry_type", sa.String(), nullable=False),
        sa.Column("details", sa.Text(), nullable=True),
        sa.Column("filed_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["mp_id"], ["mps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_transparency_entries_id", "transparency_entries", ["id"])

    op.create_table(
        "vote_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mp_id", sa.Integer(), nullable=False),
        sa.Column("motion_id", sa.Integer(), nullable=False),
        sa.Column("vote", vote_choice_enum, nullable=False),
        sa.ForeignKeyConstraint(["motion_id"], ["motions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["mp_id"], ["mps.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_vote_records_id", "vote_records", ["id"])


def downgrade() -> None:
    op.drop_index("ix_vote_records_id", table_name="vote_records")
    op.drop_table("vote_records")

    op.drop_index("ix_transparency_entries_id", table_name="transparency_entries")
    op.drop_table("transparency_entries")

    op.drop_index("ix_spending_entries_id", table_name="spending_entries")
    op.drop_table("spending_entries")

    op.drop_index("ix_speeches_id", table_name="speeches")
    op.drop_table("speeches")

    op.drop_index("ix_motions_id", table_name="motions")
    op.drop_table("motions")

    op.drop_index("ix_mps_id", table_name="mps")
    op.drop_table("mps")

    motion_classification_enum = postgresql.ENUM(
        "substantive",
        "subsidiary",
        "privileged",
        "incidental",
        name="motionclassification",
        create_type=False,
    )
    vote_choice_enum = postgresql.ENUM(
        "yea",
        "nay",
        "abstain",
        name="votechoice",
        create_type=False,
    )

    vote_choice_enum.drop(op.get_bind(), checkfirst=True)
    motion_classification_enum.drop(op.get_bind(), checkfirst=True)
