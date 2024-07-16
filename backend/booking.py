from flask_restx import Namespace, Resource, fields
from models import Booking
from flask_jwt_extended import jwt_required
from flask import Flask,request, jsonify

booking_ns = Namespace('booking', description='Namespace for booking')

# Model (serializer)
booking_model=booking_ns.model(
    "Booking",
    {
        "id":fields.Integer(),
        "title":fields.String(),
        "description":fields.String()
    }
)


@booking_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {"message":"Hello World"}


@booking_ns.route('/bookings')
class BookingsResource(Resource):
    
    @booking_ns.marshal_list_with(booking_model)
    def get(self):
        """Get all bookings"""
        
        bookings = Booking.query.all()
        
        return bookings
   
    @booking_ns.marshal_with(booking_model)
    @booking_ns.expect(booking_model)
    def post(self):
        '''Create a new booking'''
        
        data=request.get_json()
        
        new_booking=Booking(
            title=data.get('title'),
            description=data.get('description')
        )
        
        new_booking.save()
        return new_booking, 201
    

@booking_ns.route('/booking/<int:id>')
class BookingReource(Resource):
    
    @booking_ns.marshal_with(booking_model)
    def get(self,id):
        '''Get booking by id'''
        booking=Booking.query.get_or_404(id)
        
        return booking
    
    @booking_ns.marshal_with(booking_model)
    def put(self,id):
        '''Update booking by id'''
        booking_to_update=Booking.query.get_or_404(id)
        data=request.get_json()

        booking_to_update.update(data.get('title'), data.get('description'))
        
        return booking_to_update
        
        
    @booking_ns.marshal_with(booking_model)   
    def delete(self, id):
        '''Delete booking by id'''
        
        booking_to_delete=Booking.query.get_or_404(id)
        
        booking_to_delete.delete()
        
        return booking_to_delete
