from conftest import login


def test_register_returns_user_without_password(client):
    response = client.post(
        "/register",
        json={"email": "new@example.com", "password": "password123"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "new@example.com"
    assert "password" not in response.json()


def test_login_rejects_invalid_password(client, user):
    response = client.post(
        "/login",
        json={"email": user["email"], "password": "wrong-password"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid Credentials"}


def test_register_rejects_duplicate_email(client, user):
    response = client.post(
        "/register",
        json={"email": user["email"], "password": "another-password"},
    )

    assert response.status_code == 500


def test_register_rejects_missing_required_input(client):
    response = client.post("/register", json={"email": "missing-password@example.com"})

    assert response.status_code == 422


def test_login_rejects_nonexistent_user(client):
    response = client.post(
        "/login",
        json={"email": "unknown@example.com", "password": "password123"},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid Credentials"}


def test_protected_endpoint_requires_authentication(client):
    response = client.get("/hackathons")

    assert response.status_code == 401


def test_user_can_create_and_read_hackathon(client, user):
    headers = login(client)
    create_response = client.post(
        "/hackathons",
        headers=headers,
        json={"title": "Spring Hack", "description": "Build something useful"},
    )

    assert create_response.status_code == 200
    hackathon = create_response.json()
    assert hackathon["title"] == "Spring Hack"
    assert hackathon["created_by"] == user["id"]

    read_response = client.get(f"/hackathons/{hackathon['id']}", headers=headers)
    assert read_response.status_code == 200
    assert read_response.json()["id"] == hackathon["id"]


def test_missing_hackathon_returns_404(client, user):
    response = client.get("/hackathons/999", headers=login(client))

    assert response.status_code == 404
    assert response.json()["detail"] == "Details of the Hackathon is not found"


def test_team_creation_and_duplicate_membership_are_rejected(client, user):
    headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=headers,
        json={"title": "Team Event", "description": "Create teams"},
    ).json()

    first_team = client.post(
        "/teams",
        headers=headers,
        json={"name": "First Team", "hackathon_id": hackathon["id"]},
    )
    duplicate_team = client.post(
        "/teams",
        headers=headers,
        json={"name": "Second Team", "hackathon_id": hackathon["id"]},
    )

    assert first_team.status_code == 201
    assert duplicate_team.status_code == 400
    assert duplicate_team.json()["detail"] == "User is already in a team"


def test_team_creation_rejects_missing_hackathon(client, user):
    response = client.post(
        "/teams",
        headers=login(client),
        json={"name": "Orphan Team", "hackathon_id": 999},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "This Hackathon doesnot exists"


def test_submission_rejects_nonmember(client, user):
    owner_headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=owner_headers,
        json={"title": "Member Event", "description": "Membership matters"},
    ).json()
    team = client.post(
        "/teams",
        headers=owner_headers,
        json={"name": "Private Team", "hackathon_id": hackathon["id"]},
    ).json()
    client.post(
        "/register",
        json={"email": "outsider@example.com", "password": "password123"},
    )

    response = client.post(
        f"/teams/{team['id']}/submit",
        headers=login(client, "outsider@example.com"),
        json={"project_name": "Unauthorized Project", "demo_link": "https://example.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You are not member of a team"


def test_team_member_can_submit_once(client, user):
    headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=headers,
        json={"title": "Submission Event", "description": "Submit once"},
    ).json()
    team = client.post(
        "/teams",
        headers=headers,
        json={"name": "Submitters", "hackathon_id": hackathon["id"]},
    ).json()

    payload = {"project_name": "Project One", "demo_link": "https://example.com/demo"}
    first = client.post(f"/teams/{team['id']}/submit", headers=headers, json=payload)
    second = client.post(f"/teams/{team['id']}/submit", headers=headers, json=payload)

    assert first.status_code == 201
    assert first.json()["project_name"] == "Project One"
    assert second.status_code == 400
    assert second.json()["detail"] == "Team has already submitted"


def test_user_cannot_vote_for_own_team(client, user):
    headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=headers,
        json={"title": "Voting Event", "description": "Vote fairly"},
    ).json()
    team = client.post(
        "/teams",
        headers=headers,
        json={"name": "Voters", "hackathon_id": hackathon["id"]},
    ).json()
    submission = client.post(
        f"/teams/{team['id']}/submit",
        headers=headers,
        json={"project_name": "Own Project", "demo_link": "https://example.com"},
    ).json()

    response = client.post(
        f"/submissions/{submission['id']}/vote",
        headers=headers,
        json={"score": 10},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot vote for your own team"


def test_vote_score_must_be_between_one_and_ten(client, user):
    owner_headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=owner_headers,
        json={"title": "Score Event", "description": "Validate scores"},
    ).json()
    team = client.post(
        "/teams",
        headers=owner_headers,
        json={"name": "Scored Team", "hackathon_id": hackathon["id"]},
    ).json()
    submission = client.post(
        f"/teams/{team['id']}/submit",
        headers=owner_headers,
        json={"project_name": "Scored Project", "demo_link": "https://example.com"},
    ).json()
    client.post(
        "/register",
        json={"email": "judge@example.com", "password": "password123"},
    )
    judge_headers = login(client, "judge@example.com")

    response = client.post(
        f"/submissions/{submission['id']}/vote",
        headers=judge_headers,
        json={"score": 11},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Vote between 1 to 10"


def test_vote_score_must_be_at_least_one(client, user):
    owner_headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=owner_headers,
        json={"title": "Minimum Score Event", "description": "Validate minimum scores"},
    ).json()
    team = client.post(
        "/teams",
        headers=owner_headers,
        json={"name": "Minimum Score Team", "hackathon_id": hackathon["id"]},
    ).json()
    submission = client.post(
        f"/teams/{team['id']}/submit",
        headers=owner_headers,
        json={"project_name": "Minimum Score Project", "demo_link": "https://example.com"},
    ).json()
    client.post(
        "/register",
        json={"email": "minimum-score-judge@example.com", "password": "password123"},
    )

    response = client.post(
        f"/submissions/{submission['id']}/vote",
        headers=login(client, "minimum-score-judge@example.com"),
        json={"score": 0},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Vote between 1 to 10"


def test_duplicate_vote_is_rejected(client, user):
    owner_headers = login(client)
    hackathon = client.post(
        "/hackathons",
        headers=owner_headers,
        json={"title": "Duplicate Vote Event", "description": "Vote once"},
    ).json()
    team = client.post(
        "/teams",
        headers=owner_headers,
        json={"name": "Duplicate Vote Team", "hackathon_id": hackathon["id"]},
    ).json()
    submission = client.post(
        f"/teams/{team['id']}/submit",
        headers=owner_headers,
        json={"project_name": "Duplicate Vote Project", "demo_link": "https://example.com"},
    ).json()
    client.post(
        "/register",
        json={"email": "duplicate-voter@example.com", "password": "password123"},
    )
    voter_headers = login(client, "duplicate-voter@example.com")

    first = client.post(
        f"/submissions/{submission['id']}/vote",
        headers=voter_headers,
        json={"score": 8},
    )
    second = client.post(
        f"/submissions/{submission['id']}/vote",
        headers=voter_headers,
        json={"score": 9},
    )

    assert first.status_code == 201
    assert second.status_code == 400
    assert second.json()["detail"] == "You Have Already Voted"


def test_vote_rejects_missing_submission(client, user):
    response = client.post(
        "/submissions/999/vote",
        headers=login(client),
        json={"score": 8},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Submission Does Not Exists"