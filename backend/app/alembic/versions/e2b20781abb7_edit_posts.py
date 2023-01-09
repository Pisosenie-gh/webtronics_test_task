"""Edit posts

Revision ID: e2b20781abb7
Revises: 46ca34594c2a
Create Date: 2023-01-09 14:10:26.552045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2b20781abb7'
down_revision = '46ca34594c2a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_description'), 'posts', ['description'], unique=False)
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_title'), 'posts', ['title'], unique=False)
    op.drop_index('ix_items_description', table_name='items')
    op.drop_index('ix_items_id', table_name='items')
    op.drop_index('ix_items_title', table_name='items')
    op.drop_table('items')
    op.add_column('post_dislikes', sa.Column('post_id', sa.Integer(), nullable=True))
    op.drop_constraint('post_dislikes_item_id_fkey', 'post_dislikes', type_='foreignkey')
    op.create_foreign_key(None, 'post_dislikes', 'posts', ['post_id'], ['id'])
    op.drop_column('post_dislikes', 'item_id')
    op.add_column('post_likes', sa.Column('post_id', sa.Integer(), nullable=True))
    op.drop_constraint('post_likes_item_id_fkey', 'post_likes', type_='foreignkey')
    op.create_foreign_key(None, 'post_likes', 'posts', ['post_id'], ['id'])
    op.drop_column('post_likes', 'item_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_likes', sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'post_likes', type_='foreignkey')
    op.create_foreign_key('post_likes_item_id_fkey', 'post_likes', 'items', ['item_id'], ['id'])
    op.drop_column('post_likes', 'post_id')
    op.add_column('post_dislikes', sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'post_dislikes', type_='foreignkey')
    op.create_foreign_key('post_dislikes_item_id_fkey', 'post_dislikes', 'items', ['item_id'], ['id'])
    op.drop_column('post_dislikes', 'post_id')
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='items_owner_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='items_pkey')
    )
    op.create_index('ix_items_title', 'items', ['title'], unique=False)
    op.create_index('ix_items_id', 'items', ['id'], unique=False)
    op.create_index('ix_items_description', 'items', ['description'], unique=False)
    op.drop_index(op.f('ix_posts_title'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_index(op.f('ix_posts_description'), table_name='posts')
    op.drop_table('posts')
    # ### end Alembic commands ###