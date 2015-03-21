from flask import Blueprint,render_template,abort,redirect,url_for,request
from flask.ext.security import current_user,login_required
from app.models import Course,CourseReview
from app.forms import ReviewForm

review = Blueprint('review',__name__)

@review.route('/new/',methods=['GET','POST'])
#@login_required
def new_review():
    form = ReviewForm(request.form)
    course_id = request.args.get('course_id')
    course_name = request.args.get('course_name')
    if not course_id:
        return 'need to specify a course'
    course = Course.query.get(course_id)
    form = ReviewForm()
    review = CourseReview()
    if not course:
        return 404
    if course_name != course.name:
        return redirect(url_for('.new_review',
            course_id=course_id,
            course_name=course.name,
            form=form)
            )
    if form.validate_on_submit():
        form.populate_obj(review)
        print(review)
        review.save(course,current_user)
        return '<p>'+course_name + str(review) +'</p>'
    return render_template('new-review.html', form=form)

@login_required
@review.route('/edit/',methods=['GET','POST'])
def edit_review():
    review_id = request.args.get('review_id')
    if not review_id:
        return 404
    review = CourseReview.query.get(review_id)
    if not review:
        return 404

    #check if the user is the author
    if review.author != current_user:
        return 'You have no right to do this'

    form = ReviewForm(request.POST,review)
    if request.POST and form.validate():
        form.populate_obj(review)
        review.save()

    return render_template('new-review.html', form=form)
