import math
import platform


class CanvasManager():
    def selection_update_listener(self, old_selection, new_selection):
        self._selection = new_selection

        self._canvas.focus_set()

        if (old_selection and
            not self.is_background(old_selection)):

            self._canvas.itemconfig(old_selection, stipple="gray25",
                outline="black")  

            if (platform.system() == "Windows" and 
                not isinstance(old_selection, tuple)):
  
                self.convert_ovals(old_selection, self.convert_from_windows_ovals)  
    
       
        if (new_selection and
            not self.is_background(new_selection)):
            
            self._canvas.itemconfig(new_selection, stipple="gray50",
                outline="gold")   

            if (platform.system() == "Windows" and 
                not isinstance(new_selection, tuple)):  
                self.convert_ovals(new_selection, self.convert_to_windows_ovals)  

    def draw_windows_oval(self, x, y, radius, fill, tags):
       
        sides = 20
        points = []
        offsetx = x-(radius/2)
        offsety = y-(radius/2)
        ang = 2*math.pi / sides

        for i in range(sides):
            deg = (i+.5)*ang
            newx = math.sin(deg)/2.0+.5
            newy = math.cos(deg)/2.0+.5
            points.append(newx*radius+offsetx)
            points.append(newy*radius+offsety)

        return self._canvas.create_polygon(*points, fill=fill,
            outline="gold", stipple="gray50", tags=tags)

    def convert_ovals(self, selection, converter):
        regions = self._canvas.find_withtag(selection)

        for region in regions:
            tags = self._canvas.gettags(region)
            if "_shape:oval" in tags:
      
                higher = self._canvas.find_above(region)

                
                fill = self._canvas.itemcget(region, "fill")

                oval = converter(region, fill, tags)
                self._canvas.tag_raise(higher, oval)
                self._canvas.delete(region)

    def convert_to_windows_ovals(self, region, fill,  tags):
      
        coords = self._canvas.coords(region)
        width = (coords[2] - coords[0])
        height = (coords[3] - coords[1])
        x = coords[2] - (width/2)
        y = coords[3] - (height/2)

        return self.draw_windows_oval(x, y, width, fill, tags)     

    def convert_from_windows_ovals(self, region, fill,  tags):
      
        coords = self._canvas.coords(region)
        max_x = max(coords[::2])
        min_x = min(coords[::2])
        max_y = max(coords[1::2])
        min_y = min(coords[1::2])

        return self._canvas.create_oval(min_x, min_y, max_x, max_y, fill=fill, 
            stipple="gray25", tags=tags)

    def move_region(self, event):
        if (self._selection and 
            not self.is_background(self._selection)):

            if event.keysym == "Up":
                event.widget.move(self._selection, 0, -1)
            elif event.keysym == "Down":
                event.widget.move(self._selection, 0, 1)
            elif event.keysym == "Right":
                event.widget.move(self._selection, 1, 0)
            elif event.keysym == "Left":
                event.widget.move(self._selection, -1, 0)

    def scale_region(self, event):
        if (not self._selection or 
            self.is_background(self._selection)):
            return

        c = event.widget.coords(self._selection)

     
        is_polygon = len(c) > 6

        if is_polygon:
            width = max(c[::2]) - min(c[::2])
            height = max(c[1::2]) - min(c[1::2])
        else:
            width = c[2] - c[0]
            height = c[3] - c[1]

        if event.keysym == "Up":
            
            if is_polygon:
                event.widget.scale(self._selection, c[0], c[1], 1, (height+1)/height)
            else:
                event.widget.scale(self._selection, c[0], c[1], 1, (height-1)/height)
        elif event.keysym == "Down" and height > 1:
            if is_polygon:
                event.widget.scale(self._selection, c[0], c[1], 1, (height-1)/height)
            else:
                event.widget.scale(self._selection, c[0], c[1], 1, (height+1)/height)
        elif event.keysym == "Right":
            event.widget.scale(self._selection, c[0], c[1], (width+1)/width, 1)
        elif event.keysym == "Left" and width > 1:
            event.widget.scale(self._selection, c[0], c[1], (width-1)/width, 1)

    def is_background(self, selection):
        if "background" in self._canvas.gettags(selection):
            return True

        return False

    def __init__(self, canvas):
        canvas.bind('<Up>', self.move_region)
        canvas.bind('<Down>', self.move_region)
        canvas.bind('<Left>', self.move_region)
        canvas.bind('<Right>', self.move_region)
        canvas.bind('<Shift-Up>', self.scale_region)
        canvas.bind('<Shift-Down>', self.scale_region)
        canvas.bind('<Shift-Left>', self.scale_region)
        canvas.bind('<Shift-Right>', self.scale_region)

        canvas.focus_set()

        self._canvas = canvas
        self._selection = None
