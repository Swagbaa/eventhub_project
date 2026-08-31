hosting here: https://eventhub-project-yxi7.onrender.com



## შინაარსი

- [ფუნქციონალი](#ფუნქციონალი)
- [ლოკალურად გაშვება](#ლოკალურად-გაშვება)
- [ტესტირება](#ტესტირება)
- [ლოგირება](#ლოგირება)
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


