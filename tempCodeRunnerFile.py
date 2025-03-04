    # if rightSide % barWidth != 0:
    #     extraPxWidth = rightSide % barWidth

    #     barBody = pymunk.Body(1,100, pymunk.Body.STATIC)
        
    #     offset_y = (rightSide - extraPxWidth) * math.sin(math.radians(rotation))

    #     barBody.position = (rightSide, pos[1] - offset_y)
    #     barBody.angle = rotation

    #     barShape = pymunk.Poly.create_box(barBody, (barWidth, barHeight))
        
    #     space.add(barBody, barShape)
    #     bars.append(barShape)