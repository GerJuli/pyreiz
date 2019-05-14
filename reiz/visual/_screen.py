# -*- coding: utf-8 -*-
"""
Pyglet based screen and frame drawing

    
"""
import pyglet            
# %%
def get_screens():
    return pyglet.canvas.Display().get_screens()

# %%
class ExperimentalWindow(pyglet.window.Window):
    start_run = False
    paused = False
    
    def on_key_press(self, symbol, modifiers):
        """Default on_key_press handler."""
        key = pyglet.window.key
        if symbol == key.ESCAPE and not (modifiers & ~(key.MOD_NUMLOCK | 
                                                       key.MOD_CAPSLOCK | 
                                                       key.MOD_SCROLLLOCK)):
            self.dispatch_event('on_close')    
        
        if symbol == key.F5:
            self.start_run = True
        
        if symbol == key.P:
            self.paused = ~self.paused

class Canvas():
    def __init__(self, size:(int, int)=(640, 480), origin=(100, 100)):
        maxsize = (get_screens()[0].width, get_screens()[0].height)
        if size == 'full':            
            self.size = maxsize
        else:
            self.size = size    
        
        #check whether origin is outside of window
        outside = [o<0 for o in origin]
        self.origin = [o*(1-c) for o,c in zip(origin, outside)]
        
        self.start_width = size[0]
        self.start_height = size[1]
        self._create_window()

    @property
    def paused(self):
        return self.window.paused

    @property
    def start_run(self):
        return self.window.start_run

    def is_fps_feasible(self, fps, throw=True):
        if fps >= .9*self.get_fps():
            if throw:
                raise ResourceWarning('Framerate to high for monitor: decrease fps')    
            else:
                return False                  
        return True

    def get_fps(self):     
        pyglet.clock.tick()
        for i in range(0, 100, 1):
            self.window.flip()
            pyglet.clock.tick()
        return pyglet.clock.get_fps()    
    
    def _create_window(self):
        self.window = ExperimentalWindow(visible=False,
                                         vsync=True,
                                         width=self.start_width,
                                         height=self.start_height,
                                         resizable=True,
                                         caption='Experimental Framework')

        self.window.set_location(*self.origin)
        self.window.dispatch_events()
        self.window.on_close = self._on_close
        self.window.has_exit = False
    
    def _on_close(self):        
        self.window.has_exit = True
        self.window.close()
        
    def _on_key_press(symbol, modifiers):
        pass
        
    def dispatch(self):        
        self.window.dispatch_events()
        self.window.dispatch_event('on_draw')
        
    def flip(self):
        "flip the backbuffer to front  and clear the old frontbuffer"
        try:
            self.window.switch_to()        
            self.dispatch()
            self.window.flip() # flip front to backbuffer                   
            self.window.clear() #clear the current backbuffer: was the old backbuffer
        except AttributeError:
            raise Exception('Window was closed')
            
         
    def open(self):  
        if not hasattr(self, 'window'):
            self._create_window()
        self.window.set_visible(True)        
        self.window.switch_to()        
        self.dispatch()
        self.clear()        
    
    def close(self):        
        self.window.close()
        del self.window
    
    def clear(self):    
        "clear both buffers and show a black screen"
        self.flip()
        self.flip()
    
    def show(self, visual):
        "after having rendered and drawn into the backbuffer, show this"
        try:
            self.window.switch_to()              
            for v in visual:
                if v is not None:
                    v.draw(canvas=self)                
        except TypeError:
            visual.draw(canvas=self)                
        self.flip()
    
    def set_fullscreen(self):   
        self.window.set_fullscreen(fullscreen=True)
        self.flip()

    def set_windowed(self):
        self.window.set_fullscreen(fullscreen=False)
        self.flip()
        
    def get_width(self):
        return self.window.width
    
    def get_height(self):
        return self.window.height

    def get_diag(self):
        return (self.height * self.width)**0.5
        
    width = property(get_width)
    height = property(get_height)
    diag = property(get_diag)
                  
  