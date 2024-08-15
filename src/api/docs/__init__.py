from .auth import sign_in_response, get_tokens_response
from .health import health_response
from .lecturer import (
    register_lecturer_response,
    get_all_my_lecturers_response,
    get_me_lecturer_response,
    get_tokens_lecturer_response,
)
from .lecturer_request import (
    get_pending_lecturer_requests_response,
    send_lecturer_request_response,
    edit_pending_lecturer_request_response,
)
from .student import (
    register_student_response,
    update_student_response,
    get_student_response,
    get_tokens_student_response,
    get_student_response,
    get_me_student_response,
    update_student_state_response,
)
from .user import (
    get_user_response,
    request_verify_response,
    verify_email_response,
    update_user_response,
    delete_user_response,
    register_user_responses,
)
from .faculty import get_all_faculties_response
from .speciality import (
    get_specialities_by_faculty_response,
    get_all_specialities_response,
)
from .session import (
    get_sessions_response,
    get_session_response,
    delete_session_response,
)
from .taught_course_lecturer import (
    get_taught_course_by_speciality_course_responses,
    get_taught_courses_in_faculty_now_responses,
    get_taught_courses_responses,
)
from .speciality_course_lecturer import (
    get_speciality_courses_by_speciality_id_responses,
    get_speciality_courses_for_my_faculty_responses,
)
from .course_lecturer import (
    get_courses_me_responses,
    add_course_responses,
    join_existing_course_responses,
    edit_course_responses,
)
from .speicality_course_student import (
    get_speciality_courses_for_my_speciality_responses,
)
from .taught_course_admin import add_taught_course_responses
from .lecturer_request_admin import accept_pending_lecturer_request_response
from .taught_coures_student import get_taught_courses_for_me_responses
from .course_request_lecturer import (
    accept_all_freshman_requests_response,
    get_pending_requests_responses,
    accept_reject_request_response,
)
from .course_request_student import (
    get_pending_requests_response,
    send_course_request_responses,
    update_course_request_response,
)
from .enrolled_course_student import get_enrolled_courses_response
from .post_lecturer import (
    get_posts_me_responses,
    create_post_response,
    update_post_response,
    delete_post_response,
)
from .comment_lecturer import add_comment_responses, get_comments_responses
from .file_leturer import download_file_responses, upload_file_responses
from .question_lecturer import add_question_responses, get_questions_responses
