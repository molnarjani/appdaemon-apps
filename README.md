# AppDaemon apps for home automations

### Components:
  * ####alarm.py:
    * Wakes me up at alarm time fetched from HA user interface
    * Incrementally increases light brightness and music volume
 
  * ####music_client.py:
    * Controls the mopidy MPD server via jsonrpc
    * Used by alarm.py to modify volume and start playing music
    
## TODO:
   - [ ] Extract music client to a PyPI package
   - [ ] Fetch **alarm duration** from HA input
   - [ ] Fetch **max volume** from HA input
   - [ ] Add tests for checking that music and lights only turn on at alarm time
   - [ ] Add tests for checking that volume and lights increment smoothly to avoid wakeing up to full brightness or extremely loud music
