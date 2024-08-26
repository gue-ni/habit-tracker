# ClockIn

_ClockIn_ is a simple web service that is useful to track any kind of periodic
data, be it manually recording visits to the gym, or recording data points from
a sensor via a easy to use API. 

On the index page, there is a simple input UI for recording an event, picked
from a list of previous event types. Every event type has it's own page, where
there are a number of different statistics that provide insight into it.

## Data Model

Occurence would be shown in histogram, with the type between occourences
numeric values can be plotted on a graph The type determines what kind of
visualization will be available
	
Event:
	-	EventName: String
	-	EventType: Occurence | Number | Text (this is really a
		catch-all, which can also contain json or other structured
		data)
	- 	Date: DateTime Object
	-	Owner: UserId	

User:
	-	Id
	- 	Name
	-	Password
	
## Links
			
- https://medium.com/analytics-vidhya/how-to-use-flask-login-with-sqlite3-9891b3248324