from flask import Flask,request, jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from models import Booking, User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash


app=Flask(__name__)
app.config.from_object(DevConfig)

db.init_app(app)

migrate=Migrate(app,db)

api=Api(app,doc='/docs')

# Model (serializer)
booking_model=api.model(
    "Booking",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)


signup_model=api.model(
    "SignUp",
    {
        "username":fields.String(),
        "email":fields.String(),
        "password":fields.String()
    }
)


@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}


@api.route('/signup')
class SignUp(Resource):
    @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        data=request.get_json()

        username=data.get('username')

        db_user=User.query.filter_by(username=username).first()

        if db_user:
            return jsonify({'message':f'{username} already exists'})

        new_user=User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()

        return jsonify({'message':f'{username} created successfully'})


@api.route('/login')
class Login(Resource):
    def post(self):
        pass


@app.shell_context_processor
def make_shell_context():
    return {
        "db" : db,
        "Booking" : Booking
    }


@api.route('/bookings')
class BookingsResource(Resource):
    
    @api.marshal_list_with(booking_model)
    def get(self):
        """Get all bookings"""
        
        bookings = Booking.query.all()
        
        return bookings
   
    @api.marshal_with(booking_model)
    @api.expect(booking_model)
    def post(self):
        '''Create a new booking'''
        
        data=request.get_json()
        
        new_booking=Booking(
            title=data.get('title'),
            description=data.get('description')
        )
        
        new_booking.save()
        return new_booking, 201
    

@api.route('/booking/<int:id>')
class BookingReource(Resource):
    
    @api.marshal_with(booking_model)
    def get(self,id):
        '''Get booking by id'''
        booking=Booking.query.get_or_404(id)
        
        return booking
    
    @api.marshal_with(booking_model)
    def put(self,id):
        '''Update booking by id'''
        booking_to_update=Booking.query.get_or_404(id)
        data=request.get_json()

        booking_to_update.update(data.get('title'), data.get('description'))
        
        return booking_to_update
        
        
    @api.marshal_with(booking_model)   
    def delete(self, id):
        '''Delete booking by id'''
        
        booking_to_delete=Booking.query.get_or_404(id)
        
        booking_to_delete.delete()
        
        return booking_to_delete


if __name__=='__main__':
    app.run()