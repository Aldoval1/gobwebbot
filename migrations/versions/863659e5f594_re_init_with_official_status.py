"""Re-init with Official Status

Revision ID: 863659e5f594
Revises:
Create Date: 2026-02-09 01:21:13.325014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '863659e5f594'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    # User Table
    if 'user' not in tables:
        op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('first_name', sa.String(length=64), nullable=True),
        sa.Column('last_name', sa.String(length=64), nullable=True),
        sa.Column('dni', sa.String(length=20), nullable=True),
        sa.Column('password_hash', sa.String(length=256), nullable=True),
        sa.Column('badge_id', sa.String(length=20), nullable=True),
        sa.Column('department', sa.String(length=64), nullable=True),
        sa.Column('official_rank', sa.String(length=64), nullable=True),
        sa.Column('official_status', sa.String(length=20), nullable=True),
        sa.Column('selfie_filename', sa.String(length=120), nullable=True),
        sa.Column('dni_photo_filename', sa.String(length=120), nullable=True),
        sa.Column('discord_id', sa.String(length=50), nullable=True),
        sa.Column('on_duty', sa.Boolean(), nullable=True),
        sa.Column('receive_notifications', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('discord_id')
        )
        with op.batch_alter_table('user', schema=None) as batch_op:
            batch_op.create_index(batch_op.f('ix_user_badge_id'), ['badge_id'], unique=True)
            batch_op.create_index(batch_op.f('ix_user_dni'), ['dni'], unique=True)
            batch_op.create_index(batch_op.f('ix_user_first_name'), ['first_name'], unique=False)
            batch_op.create_index(batch_op.f('ix_user_last_name'), ['last_name'], unique=False)
    else:
        # Check for missing columns in existing table
        columns = [c['name'] for c in inspector.get_columns('user')]
        if 'on_duty' not in columns:
            op.add_column('user', sa.Column('on_duty', sa.Boolean(), nullable=True))
        if 'receive_notifications' not in columns:
            op.add_column('user', sa.Column('receive_notifications', sa.Boolean(), nullable=True))

    if 'appointment' not in tables:
        op.create_table('appointment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('citizen_id', sa.Integer(), nullable=True),
        sa.Column('official_id', sa.Integer(), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('reason', sa.String(length=200), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['citizen_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['official_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'business' not in tables:
        op.create_table('business',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('location_x', sa.Float(), nullable=True),
        sa.Column('location_y', sa.Float(), nullable=True),
        sa.Column('photo_filename', sa.String(length=120), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'comment' not in tables:
        op.create_table('comment',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'criminal_record' not in tables:
        op.create_table('criminal_record',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=True),
        sa.Column('crime', sa.String(length=100), nullable=True),
        sa.Column('penal_code', sa.String(length=50), nullable=True),
        sa.Column('report_text', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'traffic_fine' not in tables:
        op.create_table('traffic_fine',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=200), nullable=True),
        sa.Column('date', sa.DateTime(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('author_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['author_id'], ['user.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'criminal_record_evidence_photo' not in tables:
        op.create_table('criminal_record_evidence_photo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=120), nullable=True),
        sa.Column('record_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['record_id'], ['criminal_record.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'criminal_record_subject_photo' not in tables:
        op.create_table('criminal_record_subject_photo',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(length=120), nullable=True),
        sa.Column('record_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['record_id'], ['criminal_record.id'], ),
        sa.PrimaryKeyConstraint('id')
        )

    if 'license' not in tables:
        op.create_table('license',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('issue_date', sa.Date(), nullable=True),
        sa.Column('expiration_date', sa.Date(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('business_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['business_id'], ['business.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('license')
    op.drop_table('criminal_record_subject_photo')
    op.drop_table('criminal_record_evidence_photo')
    op.drop_table('traffic_fine')
    op.drop_table('criminal_record')
    op.drop_table('comment')
    op.drop_table('business')
    op.drop_table('appointment')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_last_name'))
        batch_op.drop_index(batch_op.f('ix_user_first_name'))
        batch_op.drop_index(batch_op.f('ix_user_dni'))
        batch_op.drop_index(batch_op.f('ix_user_badge_id'))

    op.drop_table('user')
    # ### end Alembic commands ###
