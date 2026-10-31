from sqlalchemy import create_engine,text,MetaData,Table,Column,Integer,String,ForeignKey,Float

engine = create_engine("sqlite:///db/my_db.db",echo=True)

conn = engine.connect()
meta = MetaData()

people = Table(
    "people",
    meta,
    Column('id',Integer,primary_key=True),
    Column('name',String,nullable=True),
    Column('age',Integer)
)

things = Table(
    "things",
    meta,
    Column("id",Integer,primary_key=True),
    Column("desc",String,nullable=True),
    Column("value",Float),
    Column("owner",Integer,ForeignKey('people.id'))
)

meta.create_all(engine)

insert_p = people.insert().values([
    {
        "name":"oussama",
        "age":21
    },
    {
        "name":"fatima",
        "age":25
    },
    {
        "name":"malek",
        "age":30
    },
])
insert_things = things.insert().values([
    {
        "owner":1,
        "desc" :"desc1",
        "value":213.2
    },
    {
        "owner":2,
        "desc" :"desc2",
        "value":32
    },
    {
        "owner":3,
        "desc" :"desc3",
        "value":213.2
    },
    {
        "owner":4,
        "desc" :"desc4",
        "value":213.2
    },
])

# conn.execute(insert_p)
# conn.execute(insert_things)

# conn.commit()

join_st = people.join(things,people.c.id == things.c.owner)
select_stat = people.select().with_only_columns(people.c.name,things.c.desc).select_from(join_st)

res = conn.execute(select_stat)

for r in res.fetchall():
    print(r)