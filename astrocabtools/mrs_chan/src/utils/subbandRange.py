"""
Method that calculate the subband channels that a value is in
"""

__all__ = ['obtain_sub_band']

def obtain_sub_band(value, channell):
      """ Return subband from same channel, min and max range values of each subband
      :param int value: lambda transformed value
      :param string channelL: channel where the value is located
      :return: subbands and min and max limits
      """
      #If channel is between a range of value, it is assigned

      #If channel is 1, check subband
      if channell == '1':
          if 4.87 <= value <= 5.82:
              if value < 5.62:
                  return ['1A'],[4.87], [5.82]
              else:
                  return ['1A','1B'], [4.87, 5.62], [5.82, 6.73]
          elif 5.82 < value <= 6.73:
              if value < 6.49:
                  return ['1B'], [5.82], [6.73]
              else:
                  return ['1B','1C'], [5.82, 6.49], [6.73, 7.76]
          else:
              return ['1C'], [6.49],[7.76]

      #If channel is 2, check subband
      elif channell == '2':
          if 7.45 <= value <= 8.90:
              if value < 8.61:
                  return ['2A'], [7.45], [8.90]
              else:
                  return ['2A', '2B'], [7.45, 8.61], [8.90, 10.28]
          elif 8.90 < value <=10.28:
              if value < 9.91:
                  return ['2B'], [8.61],[10.28]
              else:
                  return ['2B', '2C'], [8.61, 9.91], [10.28, 11.87]
          else:
              return ['2C'], [9.91], [11.87]

      #If channel is 2, check subband
      elif channell == '3':
          if 11.47 <=  value <= 13.67:
              if value < 13.25:
                  return ['3A'], [11.47], [13.67]
              else:
                  return ['3A', '3B'], [11.47, 13.25], [13.67, 15.80]
          elif 13.67 < value <= 15.80:
              if value < 15.30:
                  return ['3A'], [13.67], [15.80]
              else:
                  return ['3A', '3B'], [13.67, 15.30], [15.80, 18.24]
          else:
              return ['3C'], [15.30], [18.24]

      #If channel is 4, check subband
      else:
          if 17.54 <= value <= 21.10:
              if value < 20.44:
                  return ['4A'], [17.54], [21.10]
              else:
                  return ['4A', '4B'], [17.54, 20.44], [21.10, 24.72]
          elif 20.44 < value <= 24.72:
              if value < 23.84:
                  return ['4B'],[20.44], [24.72]
              else:
                  return ['4B', '4C'], [20.44, 23.84], [24.72, 28.82]
          else:
              return ['4C'], [23.84], [28.82]
