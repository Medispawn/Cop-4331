from a_star import AStar
import Adafruit_TCS34725
import smbus
import time
import math
import struct 

class goForward:
  def __init__(self):
    self.bus = smbus.SMBus(1)
    self.isLost = False
    self.nextSearchDirection = 0  # (left: 0, right: 1)
    self.directionFacing = 'north'
    self.veerSpeed = 30
    self.maxSpeed = 100
    self.aStar = AStar()
    self.tcs = Adafruit_TCS34725.TCS34725()
    self.initialLeftCount = self.aStar.read_encoders()[0]
    self.initialRightCount = self.aStar.read_encoders()[1]
    # self.aStar.reset_encoders()
    self.countLeft = 0
    self.countRight = 0
    self.lastCountLeft = 0
    self.lastCountRight = 0
    self.countSignLeft = 1
    self.countSignRight = -1
  def motors(self, lspeed, rspeed):
    self.aStar.motors(lspeed, rspeed)
  def grabdifference(self):
    countLeft, countRight = self.aStar.read_encoders()
    diff = math.fabs(countLeft - countRight)
    return diff

  def reset(self):
    self.countLeft = 0
    self.countRight = 0

  def reset_encoders(self):
    self.write_pack(24, 'B', 1)

  def write_pack(self, address, format, *data):
    data_array = map(ord, list(struct.pack(format, *data)))
    print(data_array)
    self.bus.write_i2c_block_data(20, address, data_array)
    time.sleep(.0001)

  def goForwardtwo(self):
    x = self.maxSpeed
    self.motors(x, x)
    grabEncoders = self.readCounts()
    # print(grabEncoders)
    diff = math.fabs(grabEncoders[0] - grabEncoders[1])
    # print(diff)
    while(diff  >  3):
      grabEncoders = self.readCounts()
      diff = math.fabs(grabEncoders[0] - grabEncoders[1])
      x-=1
      # print(grabEncoders)
      # print(diff)
      if(grabEncoders[0] < grabEncoders[1]):
        self.motors(self.maxSpeed, x)
        time.sleep(2.0/1000.0)
      elif(grabEncoders[0] > grabEncoders[1]):
        self.motors(x, self.maxSpeed)
        time.sleep(2.0/1000.0)
    self.motors(self.maxSpeed, self.maxSpeed)

  def readCounts(self):
    differ = self.grabdifference()
    countRight = 0
    countLeft = 0
    countLeft, countRight = self.aStar.read_encoders()
    Left = countLeft
    Right = countRight
    if(differ < 100):
      countLeft, countRight = self.aStar.read_encoders()
      Right = countRight
      Left = countLeft
    else:
      maximum = max(countRight,countLeft)
      print(maximum)
      if(countRight == maximum):
        Right = Right - differ
      else:
        Left = Left - differ

    # print(countLeft, countRight)
    # diffLeft = (countLeft - self.lastCountLeft) % 0x10000
    # if diffLeft >= 0x8000:
    #     diffLeft -= 0x10000
        
    # diffRight = (countRight - self.lastCountRight) % 0x10000
    # if diffRight >= 0x8000:
    #     diffRight -= 0x10000
        
    # self.countLeft += self.countSignLeft * diffLeft
    # self.countRight += self.countSignRight * diffRight

    # self.lastCountLeft = countLeft
    # self.lastCountRight = countRight
    print(Right,Left)
    return countLeft, countRight

