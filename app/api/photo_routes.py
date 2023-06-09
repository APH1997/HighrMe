from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Photo, User, Album, Comment, Reply
from app.forms import PhotoForm, EditPhotoForm, CreateAlbumForm, EditAlbumForm, CommentForm
from app.api.aws_helpers import get_unique_filename, upload_file_to_s3, remove_file_from_s3

photo_routes = Blueprint('photos', __name__)

# Get All Photos
@photo_routes.route('/all')
@login_required
def all_photos():
    """
    Query for all photos and returns them
    in a list of dictionaries WITH authors, comments, and albums;
    This route populates the home feed.
    """
    photos = Photo.query.all()

    return [photo.to_dict() for photo in photos]



# Get All Photos by User Id
@photo_routes.route('/user/<int:userId>')
@login_required
def all_user_photos(userId):
    """
    Query for all photos where author_id == userId
    This route populates a user page's photo stream tab
    """
    user = User.query.get(userId)
    if not user:
        return {'error':'User could not be found'}

    photos = Photo.query.filter(Photo.author_id == userId).all()
    return [photo.to_dict() for photo in photos]



# Get Photo by Photo Id
@photo_routes.route('/<int:photoId>')
@login_required
def get_photo_by_id(photoId):
    """
    Query for one photo by it's Id
    Return in a dictionary with comments, albums, author
    """
    photo = Photo.query.get(photoId)
    if photo:
        return photo.to_dict()
    else:
        return {"error": "Requested photo could not be found"}, 404

# Post Photo
@photo_routes.route('/new', methods=['POST'])
@login_required
def post_photo():
    """
    Takes form data, validates against FlaskForm
    If succesful, uploads to AWS and returns new photo.to_dict_no_author()
    If fail, return error dictionary
    """
    form = PhotoForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        photo = form.data["photo"]
        photo.filename = get_unique_filename(photo.filename)
        upload = upload_file_to_s3(photo)

        if "url" not in upload:
            return upload["errors"]

        photo_url = upload["url"]

        new_photo = Photo(
            author_id = form.data["author_id"],
            aws_url = photo_url,
            caption = form.data["caption"],
            description = form.data["description"]
        )

        db.session.add(new_photo)
        db.session.commit()
        return jsonify(new_photo.to_dict())
    else:
        return {"errors": form.errors}, 400

# Edit Photo by Id
@photo_routes.route('/<int:photoId>/edit', methods=['PUT'])
@login_required
def edit_photo(photoId):
    """
    Takes form data, validates against Flask Form
    Queries for photo and updates attributes
    If there is a photo submitted with edit form,
    removes current photo from bucket and uploads given photo
    """
    form = EditPhotoForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        target_photo = Photo.query.get(photoId)

        if form.data["photo"] is not None:
            photo = form.data["photo"]
            photo.filename = get_unique_filename(photo.filename)
            upload = upload_file_to_s3(photo)

            if "url" not in upload:
                return upload["errors"]

            new_photo_url = upload["url"]

            #Upload succeeded, we can remove old photo
            remove_file_from_s3(target_photo.aws_url)

            target_photo.aws_url = new_photo_url

        target_photo.caption = form.data["caption"]
        target_photo.description = form.data["description"]

        db.session.commit()

        return jsonify(target_photo.to_dict())
    else:
        return {"errors": form.errors}, 400


# Delete Photo by Id
@photo_routes.route('/<int:photoId>/delete', methods=['DELETE'])
@login_required
def delete_photo(photoId):
    """
    Queries for photo by id and deletes it;
    If last photo in an album, deletes it;
    Removes file from bucket
    """
    target = Photo.query.get(photoId)
    if not target:
        return {"error":"Photo could not be found"}, 404


    # Check each album if target is last photo
    albums = target.photo_albums
    for album in albums:
        if len(album.album_photos) == 1:
            db.session.delete(album)

    #delete the target from db and bucket
    aws_url = target.aws_url
    db.session.delete(target)
    remove_file_from_s3(aws_url)

    db.session.commit()

    return {
        "message":"Photo Deleted"
    }

# Create Album and Add Photos
@photo_routes.route('/album/new', methods=['POST'])
@login_required
def create_album():
    """
    Creates album from author_id, title;
    queries for all photo id's from form field,
    sets album.album_photos to list of photos
    If cover photo not chosen, defaults to first
    """
    form = CreateAlbumForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        new_album = Album(
            author_id = form.data["author_id"],
            title = form.data["title"]
        )
        if form.data["description"]:
            new_album.description = form.data["description"]

        photoIdList = [int(id) for id in form.data["photos"].split(',')]
        new_album.album_photos = Photo.query.filter(Photo.id.in_(photoIdList)).all()
        new_album.cover_photo_url = new_album.album_photos[0].aws_url

        db.session.add(new_album)
        db.session.commit()

        return {"newAlbumId": new_album.id}
    else:
        return form.errors, 400

# GET ALL ALBUMS
@photo_routes.route('/albums/all')
@login_required
def get_all_albums():
    albums = Album.query.all()
    return [album.to_dict() for album in albums]

@photo_routes.route('/albums/<int:albumId>/edit', methods=['PUT'])
@login_required
def edit_album(albumId):
    """
    Instantiates EditAlbum flask form
    Queries for album by id
    Updates title, description, and/or photos
    """
    form = EditAlbumForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        album = Album.query.get(albumId)
        album.title = form.data["title"]
        if form.data["description"]:
            album.description = form.data["description"]

        photoIdList = form.data["photos"].split(',')
        album.album_photos = Photo.query.filter(Photo.id.in_(photoIdList)).all()

        db.session.commit()
        return jsonify(album.to_dict())
    else:
        return form.errors, 400

@photo_routes.route('/albums/<int:albumId>/delete', methods=['DELETE'])
@login_required
def delete_album(albumId):
    """
    Queries for album by id
    Deletes it - Photos are not deleted
    """
    target = Album.query.get(albumId)
    db.session.delete(target)
    db.session.commit()

    return {
        "message":"Album Deleted"
    }


# PHOTO COMMENTS
@photo_routes.route('/<int:photoId>/comments/new', methods=["POST"])
@login_required
def create_comment(photoId):
    """
    Queries for photo by Id
    constructs comment with form data after validation
    Then adds to photo with
    Returns photo.to_dict() for reducer to update
    """
    form = CommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        target_photo = Photo.query.get(photoId)
        new_comment = Comment(
            author = current_user,
            photo = target_photo,
            content = form.data["content"]
        )
        db.session.add(new_comment)
        db.session.commit()

        return target_photo.to_dict()
    else:
        return form.errors

@photo_routes.route("/comments/<int:commentId>/edit", methods=["PUT"])
@login_required
def update_comment(commentId):
    """
    Queries for comment by id
    sets comment.content = content from formdata
    Queries for updated photo and return to_dict()
    """
    form = CommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        comment = Comment.query.get(commentId)
        comment.content = form.data["content"]
        db.session.commit()

        photo = Photo.query.get(comment.photo_id)
        return photo.to_dict()
    else:
        return form.errors, 400




@photo_routes.route('/<int:photoId>/comments/<int:commentId>/delete', methods=["DELETE"])
@login_required
def delete_comment(photoId, commentId):
    """
    Queries for photo by id
    and list comprehends photo.comments
    to remove comment by id
    returns photo.to_dict() for reducer to update
    """
    target_comment = Comment.query.get(commentId)
    db.session.delete(target_comment)
    db.session.commit()

    target_photo = Photo.query.get(photoId)
    return target_photo.to_dict()


# COMMENT REPLIES
@photo_routes.route('comments/<int:commentId>/new', methods=["POST"])
@login_required
def reply_to_comment(commentId):
    """
    Takes form data containing reply content,
    Queries for parent comment by id,
    creates new reply using comment as parent
    and current user as author.
    Queries for photo and returns it to update store
    """
    form = CommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        parent_comment = Comment.query.get(commentId)
        new_reply = Reply(
                    author = current_user,
                    parent = parent_comment,
                    content = form.data["content"]
                    )
        db.session.add(new_reply)
        db.session.commit()

        photo = Photo.query.get(parent_comment.photo.id)
        return photo.to_dict()
    else:
        return form.errors, 400



@photo_routes.route('comments/replies/<int:replyId>/edit', methods=["PUT"])
@login_required
def edit_reply(replyId):
    """
    Takes form data containing new content
    Queries for reply by id and overwrites content with form data
    Queries for photo and returns in a dictionary with updated comments/replies
    """
    form = CommentForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        target_reply = Reply.query.get(replyId)
        target_reply.content = form.data["content"]
        db.session.commit()

        photo = Photo.query.get(target_reply.parent.photo.id)
        return photo.to_dict()
    else:
        return form.errors, 400


@photo_routes.route('comments/replies/<int:replyId>/delete', methods=["DELETE"])
@login_required
def delete_reply(replyId):
    """
    Queries for reply by id and deletes it.
    Queries for parent photo and returns in a dictionary
    to update store
    """
    target = Reply.query.get(replyId)
    photoId = target.parent.photo.id

    db.session.delete(target)
    db.session.commit()

    photo = Photo.query.get(photoId)

    return photo.to_dict()
