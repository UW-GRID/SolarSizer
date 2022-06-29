User Story

Who? Individual with basic knowledge of solar panels and a simple electronic grid. 
What do they want to do? Want to know the components needed to match their power needs, the cost of the system, and the cost of maintenance.
What needs and desires do they want for the tool? Want to input a location and a power load profile and get an output on the equipment and costs
What is their skill level? No technical background 


Who? GRID Member or a member from another solar installation group 
What do they want to do? Update the solar sizing software using data collected from a testbed 
What needs and desires do they want for the tool? Well organized code that is easy to follow and alter
What is their skill level? Enginnering or other technical background 


#####################################################

Use Case
User: Input both a location (lat, lon) and a load profile
Interface: [if a viable location] displays solar panel surface area, size/capacity components needed, average cost
           [if not location] display "Not a valid location. Try again."

Use Case: Retrieve solar irradiance
    What it does: finds the closest lat, lon to the input lat, lon
                  retrieves irradiance at that location
    Inputs: (lat,lon) (tuple of float)
    Outputs: Irradiance measurement (float)


Use Case: Find specs
    What it does: Produces necessary specifications for solar panel as well as size/capacity of components needed. Uses SAM model. 
    Input: Irradiance (float)
    Output: Panel specs (list of strings)


Use Case: Find cost
    What it does: Produce average cost for all components based on input data on current market market price
    Input: List of components (list of strings)
    Output: Price for each component (list of floats)


Use Case: Display
    What it does: Shows the user the component information and pricing estimate
    Input: Price for each component (list of floats) and panel specs (list of string) 
    Output: Display of the input



