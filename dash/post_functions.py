def get_post_tags(post_id):
    term_real = Term_Relationship.query.filter_by(post_id=post_id).all()
    tags = []
    for real in term_real:
        term_id = Term_Taxonomy.query.filter((Term_Taxonomy.id == real.term_taxonomy_id) and (Term_Taxonomy.taxonomy == 'tag')).first().term_id
        tags.append(Term.query.filter_by(id = term_id).first().slug)
    return tags

@app.route('/admin/posts/blog/edit_post/<int:post_id>', methods=['POST', 'GET'])
def edit_post(post_id):
    if 'authenticated' in session:
        if 'user' in session:
            cats = Term_Taxonomy.query.filter_by(taxonomy='category').all()
            cat_ids = []
            for cat in cats:
                cat_ids.append(cat.term_id)
            categories = [] 
            for id in cat_ids:
                term = Term.query.filter_by(id=id).first().name
                categories.append(term)
            post = {}
            post['meta'] = Post_Meta.query.filter_by(post_id=post_id).all()
            post['post'] = Post.query.filter_by(id=post_id).first()
            post['author'] = Blog_User.query.filter_by(id=post['post'].author_id).first()
           
            return render_template('admin/dash/pages/post-edit.html', tags=get_post_tags(post_id), user=session.get('user'), post_action='editing', pagename='Edit Blog Post', parent_post='active', avatar=get_user_avatar(session.get('user')['id']), post_active='active', images=get_uploads(), categories=categories, bodyClass="page-post-edit", post=post)
    return redirect(url_for('login'))
