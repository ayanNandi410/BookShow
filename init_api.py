# Api initialization
from flask_restful import Resource, Api
from api.venueApi import VenueAPI, VenueListByCityApi, VenueListByNameApi
from api.showApi import ShowAPI, ListShowByNameApi, ListShowByVenueApi
from api.cityApi import  GetAllCitiesApi
from api.allocationApi import AllocationAPI
from api.bookingApi import BookTicketAPI
    
def getConfiguredApi(app):
    apiV = Api(app)

    apiV.add_resource(VenueAPI,"/api/venue","/api/venue/<string:name>",endpoint="/venue")
    apiV.add_resource(VenueListByCityApi,"/api/venues/byCity/<string:city>",endpoint="/venues/byCity/<city>")
    apiV.add_resource(VenueListByNameApi,"/api/venues/byName/<string:name>",endpoint="/venues/byName/<name>")
    
    apiV.add_resource(GetAllCitiesApi,"/api/city/all",endpoint="/city")

    apiV.add_resource(ShowAPI,"/api/show","/api/show/<string:name>",endpoint="/show")
    apiV.add_resource(ListShowByVenueApi,"/api/shows/byVenue/<string:venue>",endpoint="/shows/byVenue/<venue>")
    apiV.add_resource(ListShowByNameApi,"/api/shows/byName/<string:name>",endpoint="/shows/byName/<name>")
    
    apiV.add_resource(AllocationAPI,"/api/allocation",endpoint="/allocation")

    apiV.add_resource(BookTicketAPI,"/api/booking/<string:email>",endpoint="/booking")
    
    return apiV