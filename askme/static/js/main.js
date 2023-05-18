function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".love-btn-heart").on('click', function (ev) {
    const request = new Request(
        'http://127.0.0.1:8000/vote_up',
        {
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
            },
            method: 'POST',
            body: 'question_id=' + $(this).data('id'),
        }
    );

    fetch(request).then(
        response => {
            if (response.ok) {
                return response.json().then(
                    response_json => $(this).find('.badge').text(response_json.new_rating)
                );
            } else {
                return response.json().then(
                    error_json => {
                        console.log(error_json.error);
                    }   
                );
            }
        }
    );
});
