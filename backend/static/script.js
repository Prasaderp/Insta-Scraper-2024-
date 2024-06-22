document.addEventListener('DOMContentLoaded', function () {
    const profileForm = document.getElementById('profileForm');
    const hashtagForm = document.getElementById('hashtagForm');
    const profileError = document.getElementById('profileError');
    const hashtagError = document.getElementById('hashtagError');

    profileForm.addEventListener('submit', function (e) {
        e.preventDefault();
        profileError.style.display = 'none';
        const usernameInput = document.getElementById('username');
        if (usernameInput.value.trim() === '') {
            profileError.style.display = 'block';
            return;
        }
        setLoadingState(profileForm, true);
        const formData = new FormData(profileForm);
        fetch('/profile', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('profileResult').innerHTML = data;
            setLoadingState(profileForm, false);
        })
        .catch(error => {
            console.error('Error:', error);
            setLoadingState(profileForm, false);
        });
    });

    hashtagForm.addEventListener('submit', function (e) {
        e.preventDefault();
        hashtagError.style.display = 'none';
        const hashtagInput = document.getElementById('hashtag');
        if (hashtagInput.value.trim() === '') {
            hashtagError.style.display = 'block';
            return;
        }
        setLoadingState(hashtagForm, true);
        const formData = new FormData(hashtagForm);
        fetch('/hashtag', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            document.getElementById('hashtagResult').innerHTML = data;
            setLoadingState(hashtagForm, false);
        })
        .catch(error => {
            console.error('Error:', error);
            setLoadingState(hashtagForm, false);
        });
    });

    function setLoadingState(form, isLoading) {
        const button = form.querySelector('button[type="submit"]');
        if (isLoading) {
            button.classList.add('loading');
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            button.disabled = true;
        } else {
            button.classList.remove('loading');
            if (form === profileForm) {
                button.textContent = 'Search Profile';
            } else if (form === hashtagForm) {
                button.textContent = 'Search Hashtag';
            }
            button.disabled = false;
        }
    }
});
