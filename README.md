# EventHub

ღონისძიებების განცხადება-ძიების ვებ პორტალი, აგებული Flask-ზე.
პროექტი მოიცავს რეგისტრაცია/ავტორიზაციას, ღონისძიებების CRUD-ს
(მხოლოდ საკუთარი ჩანაწერების რედაქტირება/წაშლა), როლებზე
დაფუძნებულ დაშვებებს, გარე API ინტეგრაციას (OpenWeatherMap),
ლოგირებას და unit ტესტებს.

## შინაარსი

- [ფუნქციონალი](#ფუნქციონალი)
- [ტექნოლოგიები](#ტექნოლოგიები)
- [პროექტის სტრუქტურა](#პროექტის-სტრუქტურა)
- [ლოკალურად გაშვება](#ლოკალურად-გაშვება)
- [გარემოს ცვლადები (.env)](#გარემოს-ცვლადები-env)
- [ტესტირება](#ტესტირება)
- [ლოგირება](#ლოგირება)
- [GitHub-ზე ატვირთვა](#github-ზე-ატვირთვა)
- [Production დეპლოი (Render.com)](#production-დეპლოი-rendercom)
- [მოთხოვნების შესაბამისობა](#მოთხოვნების-შესაბამისობა)

## ფუნქციონალი

- რეგისტრაცია (სახელი/ელფოსტა/პაროლი/გამეორება) და ავტორიზაცია
- ავტორიზაციის გარეშე: ღონისძიებების ნახვა და About გვერდი
- ავტორიზებულებისთვის: Add Event, Logout, Profile
- ღონისძიების დამატება: სათაური, მოკლე/სრული აღწერა, ლოკაცია,
  თარიღი, ბილეთის ფასი, ორგანიზატორი, კატეგორია
- ღონისძიებების ბარათები (author-ზე გადასვლის ბმულით) + "Read More"
- საკუთარი ღონისძიების რედაქტირება/წაშლა; სხვისი — მხოლოდ ნახვა
  (რედაქტირების/წაშლის მცდელობაზე 403)
- ნავიგაცია: About, Events, Add Event, Login/Register, Profile
- 404 და 500 შეცდომების გვერდები (+ 403, დამატებით)
- ყველა ფორმა CSRF დაცვით (Flask-WTF)
- პროფილი: სურათი, სახელი, ელფოსტა — რედაქტირებადი
- ღონისძიებები დალაგებულია განთავსების თარიღით (+ ფილტრი
  კატეგორიით, სორტირება თარიღით)
- კატეგორიები: Music, Tech, Art, Sport, Education, Business, Other
- გარე API: OpenWeatherMap — ღონისძიების გვერდზე ჩანს მიმდინარე
  ამინდი ლოკაციისთვის (მონაცემი მოდის დინამიურად)

## ტექნოლოგიები

Flask 3, Flask-SQLAlchemy, Flask-Login, Flask-WTF, WTForms,
SQLite (dev/test) / PostgreSQL (production-ready), Bootstrap 5,
Pillow (სურათების დამუშავება), requests (გარე API), pytest.

## პროექტის სტრუქტურა

```
eventhub/
├── app/
│   ├── __init__.py        # app factory, error handlers, logging setup
│   ├── extensions.py      # db, login_manager, csrf
│   ├── models.py          # User, Event
│   ├── forms.py           # WTForms ფორმები
│   ├── utils.py           # ლოგირება, სურათის შენახვა, weather API
│   ├── routes/
│   │   ├── main.py        # events feed, about, event detail
│   │   ├── auth.py        # register/login/logout
│   │   ├── events.py      # add/edit/delete event
│   │   └── profile.py     # profile view/edit
│   ├── templates/
│   └── static/
├── tests/                  # pytest: routes, login, permissions
├── logs/                   # eventhub.log (runtime log ფაილი)
├── config.py
├── run.py
├── requirements.txt
├── Procfile                # production-ში გასაშვებად (gunicorn)
└── .env.example
```

## ლოკალურად გაშვება

1. შექმენით ვირტუალური გარემო და დააინსტალირეთ დამოკიდებულებები:

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows-ზე: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. დააკოპირეთ `.env.example` → `.env` და შეავსეთ მნიშვნელობები
   (იხ. შემდეგი სექცია).

3. გაუშვით აპლიკაცია:

   ```bash
   python run.py
   ```

   გვერდი ხელმისაწვდომი იქნება: `http://127.0.0.1:5000`

   პირველივე გაშვებაზე ავტომატურად შეიქმნება `instance/eventhub.db`
   (SQLite) საჭირო ცხრილებით.

## გარემოს ცვლადები (.env)

| ცვლადი                | აღწერა                                                        |
|------------------------|----------------------------------------------------------------|
| `SECRET_KEY`           | გრძელი შემთხვევითი სტრიქონი (სესიების/CSRF-ის დასაცავად)       |
| `DATABASE_URL`         | არასავალდებულო — production-ში PostgreSQL-ის connection string |
| `OPENWEATHER_API_KEY`  | უფასო გასაღები [openweathermap.org/api](https://openweathermap.org/api)-დან |

**შენიშვნა:** თუ `OPENWEATHER_API_KEY` არ არის მითითებული ან API
მოთხოვნა ჩავარდება, ღონისძიების გვერდი მაინც ჩაიტვირთება — უბრალოდ
აჩვენებს "ამინდი ამჟამად მიუწვდომელია" და შეცდომას ჩაწერს ლოგში,
ვებ-გვერდი არ ავარდება.

## ტესტირება

პროექტს აქვს pytest-ზე დაფუძნებული ტესტების ნაკრები (`tests/`):

```bash
pytest -v
```

მოიცავს:

- **Route ტესტები** (`test_routes.py`) — მთავარი გვერდი, About,
  ღონისძიების დეტალები, 404 არარსებული გვერდისთვის
- **Login ტესტები** (`test_login.py`) — რეგისტრაცია, წარმატებული/
  წარუმატებელი შესვლა, გამოსვლა
- **უფლებების ტესტები** (`test_permissions.py`) — სხვისი
  ღონისძიების რედაქტირების/წაშლის მცდელობაზე 403 და მონაცემი
  ბაზაში უცვლელი რჩება

ტესტები დამოუკიდებელი in-memory SQLite ბაზით მუშაობს და არ ეხება
რეალურ `instance/eventhub.db` ფაილს.

## ლოგირება

ყველა მნიშვნელოვანი მოქმედება იწერება ფაილში `logs/eventhub.log`:

- წარმატებული ავტორიზაცია
- წარუმატებელი ავტორიზაცია
- ახალი ღონისძიების დამატება
- ღონისძიების რედაქტირება/წაშლა (და უნებართვო მცდელობები — 403)
- გარე (weather) API-ის შეცდომები

## GitHub-ზე ატვირთვა

```bash
cd eventhub
git init
git add .
git commit -m "Initial commit: EventHub Flask app"
git branch -M main
git remote add origin https://github.com/<თქვენი-username>/eventhub.git
git push -u origin main
```

`.gitignore` უკვე გამორიცხავს `.env`, ვირტუალურ გარემოს, SQLite
ფაილს, ატვირთულ სურათებს და ლოგებს — ისე, რომ საიდუმლო
მონაცემები არ აღმოჩნდეს repo-ში.

## Production დეპლოი (Render.com)

დავალება მოითხოვს აპლიკაციის განთავსებას რეალურ URL-ზე. უმარტივესი
უფასო გზა — [Render](https://render.com):

1. აიტვირთეთ პროექტი GitHub-ზე (იხ. ზემოთ).
2. Render-ზე: **New → Web Service** → დაუკავშირდით თქვენს GitHub
   repo-ს.
3. მიუთითეთ:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app`
4. **Environment** სექციაში დაამატეთ `SECRET_KEY` და
   `OPENWEATHER_API_KEY` (და, PostgreSQL-ის გამოყენების შემთხვევაში,
   `DATABASE_URL` — Render-ს შეუძლია უფასო Postgres ბაზის შექმნაც).
5. Deploy-ის შემდეგ მიიღებთ საჯარო URL-ს, მაგ.
   `https://eventhub-xxxx.onrender.com`.

ალტერნატივები იგივე პრინციპით: Railway.app, PythonAnywhere,
Fly.io — ყველგან საკმარისია `requirements.txt` + `Procfile`/start
command + გარემოს ცვლადები.

## მოთხოვნების შესაბამისობა

| კომპონენტი                        | სად არის განხორციელებული                         |
|------------------------------------|---------------------------------------------------|
| Flask Project Structure            | `app/` factory + blueprints                        |
| Database Models                    | `app/models.py` (User, Event)                      |
| Auth (hashing, register/login/out) | `app/routes/auth.py`, `werkzeug.security`          |
| CRUD (own events only)             | `app/routes/events.py` (author_id შემოწმება)       |
| Templates / Jinja2 / Bootstrap     | `app/templates/*`, Bootstrap 5 CDN                  |
| Role logic (permissions)           | `events.py` — `abort(403)` არა-ავტორისთვის          |
| Error handlers (404 + 500)         | `app/__init__.py` + `templates/errors/*`           |
| Event list + single event view     | `main.py` (`index`, `event_detail`)                |
| Filters / Sorting                  | `index.html` + `main.py` (category, sort)          |
| External API Integration           | `app/utils.py` `get_weather()` (OpenWeatherMap)    |
| Logging                            | `app/utils.py` `setup_logging()` → `logs/eventhub.log` |
| Testing (min. 3 ტესტი)             | `tests/` (14 ტესტი სამივე კატეგორიაზე)             |
