from app.database import engine, Base, SessionLocal
from app.models.entities import Department, AuthorityRule, User
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(f"salt_civicfix_{password}".encode()).hexdigest()


def seed_database(db: SessionLocal = None):
    Base.metadata.create_all(bind=engine)
    close_at_end = False
    if db is None:
        db = SessionLocal()
        close_at_end = True


    try:
        # 1. Seed Demo Departments
        departments_data = [
            {"code": "ROAD", "name": "Road & Infrastructure Department", "contact_email": "roads@demo.civic.gov", "base_sla_hours": 72},
            {"code": "SANITATION", "name": "Sanitation & Solid Waste Management", "contact_email": "waste@demo.civic.gov", "base_sla_hours": 24},
            {"code": "STREETLIGHT", "name": "Electrical & Street Lighting Department", "contact_email": "lighting@demo.civic.gov", "base_sla_hours": 48},
            {"code": "WATER", "name": "Water Supply & Sewerage Board", "contact_email": "water@demo.civic.gov", "base_sla_hours": 24},
            {"code": "DRAINAGE", "name": "Stormwater Drainage & Flood Control", "contact_email": "drainage@demo.civic.gov", "base_sla_hours": 48},
            {"code": "HORTICULTURE", "name": "Parks & Horticulture Department", "contact_email": "trees@demo.civic.gov", "base_sla_hours": 12},
        ]

        dept_map = {}
        for d_info in departments_data:
            existing = db.query(Department).filter(Department.code == d_info["code"]).first()
            if not existing:
                dept = Department(
                    code=d_info["code"],
                    name=d_info["name"],
                    contact_email=d_info["contact_email"],
                    base_sla_hours=d_info["base_sla_hours"]
                )
                db.add(dept)
                db.commit()
                db.refresh(dept)
                dept_map[d_info["code"]] = dept.id
            else:
                dept_map[d_info["code"]] = existing.id

        # 2. Seed Authority Rules
        rules_data = [
            {"category": "Pothole", "dept": "ROAD"},
            {"category": "Damaged Road", "dept": "ROAD"},
            {"category": "Damaged Footpath", "dept": "ROAD"},
            {"category": "Garbage", "dept": "SANITATION"},
            {"category": "Overflowing Garbage Bin", "dept": "SANITATION"},
            {"category": "Broken Streetlight", "dept": "STREETLIGHT"},
            {"category": "Water Leakage", "dept": "WATER"},
            {"category": "Drainage Problem", "dept": "DRAINAGE"},
            {"category": "Fallen Tree", "dept": "HORTICULTURE"}
        ]

        for r_info in rules_data:
            d_id = dept_map.get(r_info["dept"])
            if d_id:
                existing_rule = db.query(AuthorityRule).filter(AuthorityRule.category == r_info["category"]).first()
                if not existing_rule:
                    rule = AuthorityRule(department_id=d_id, category=r_info["category"], priority=1)
                    db.add(rule)

        # 3. Seed Demo Users (Citizen & Admin)
        admin_user = db.query(User).filter(User.email == "admin@civicfix.demo").first()
        if not admin_user:
            admin = User(
                email="admin@civicfix.demo",
                password_hash=hash_password("admin123"),
                full_name="CivicFix Admin",
                role="ADMIN"
            )
            db.add(admin)

        citizen_user = db.query(User).filter(User.email == "citizen@civicfix.demo").first()
        if not citizen_user:
            citizen = User(
                email="citizen@civicfix.demo",
                password_hash=hash_password("citizen123"),
                full_name="Jane Citizen",
                role="CITIZEN"
            )
            db.add(citizen)

        db.commit()
        print("Database seeding completed successfully.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        if close_at_end:
            db.close()

if __name__ == "__main__":
    seed_database()
