import win32com.client
pl = win32com.client.Dispatch("PrairieLink.Application")
pl.Connect("10.156.138.56")