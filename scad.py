import copy
import opsc
import oobb
import oobb_base
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    parts = []

    typ = kwargs.get("typ", "")

    if typ == "":
        #setup    
        #typ = "all"
        typ = "fast"
        #typ = "manual"

    oomp_mode = "project"
    #oomp_mode = "oobb"

    if typ == "all":
        filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr"]; oomp_run = True
        #filter = ""; save_type = "all"; navigation = True; overwrite = True; modes = ["3dpr", "laser", "true"]
    elif typ == "fast":
        filter = ""; save_type = "none"; navigation = False; overwrite = True; modes = ["3dpr"]; oomp_run = False
    elif typ == "manual":
    #filter
        filter = ""
        #filter = "double"

    #save_type
        save_type = "none"
        #save_type = "all"
        
    #navigation        
        #navigation = False
        navigation = True    

    #overwrite
        overwrite = True
                
    #modes
        #modes = ["3dpr", "laser", "true"]
        modes = ["3dpr"]
        #modes = ["laser"]    

    #oomp_run
        oomp_run = True
        #oomp_run = False    

    #adding to kwargs
    kwargs["filter"] = filter
    kwargs["save_type"] = save_type
    kwargs["navigation"] = navigation
    kwargs["overwrite"] = overwrite
    kwargs["modes"] = modes
    kwargs["oomp_mode"] = oomp_mode
    kwargs["oomp_run"] = oomp_run
    
       
    # project_variables
    if True:
        pass
    
    # declare parts
    if True:

        directory_name = os.path.dirname(__file__) 
        directory_name = directory_name.replace("/", "\\")
        project_name = directory_name.split("\\")[-1]
        #max 60 characters
        length_max = 40
        if len(project_name) > length_max:
            project_name = project_name[:length_max]
            #if ends with a _ remove it 
            if project_name[-1] == "_":
                project_name = project_name[:-1]
                
        #defaults
        kwargs["size"] = "oobb"
        kwargs["width"] = 1
        kwargs["height"] = 1
        kwargs["thickness"] = 3
        #oomp_bits
        if oomp_mode == "project":
            kwargs["oomp_classification"] = "project"
            kwargs["oomp_type"] = "github"
            kwargs["oomp_size"] = "oomlout"
            kwargs["oomp_color"] = project_name
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""
        elif oomp_mode == "oobb":
            kwargs["oomp_classification"] = "oobb"
            kwargs["oomp_type"] = "part"
            kwargs["oomp_size"] = ""
            kwargs["oomp_color"] = ""
            kwargs["oomp_description_main"] = ""
            kwargs["oomp_description_extra"] = ""
            kwargs["oomp_manufacturer"] = ""
            kwargs["oomp_part_number"] = ""

        part_default = {} 
       
        part_default["project_name"] = project_name
        part_default["full_shift"] = [0, 0, 0]
        part_default["full_rotations"] = [0, 0, 0]
        

        types = []
        part = {}
        part["width"] = 3
        part["height"] = 3
        part["thickness"] = 12
        part["name"] = "toy_bubble_wand_33_mm_diameter"
        types.append(part)

        part = {}
        part["width"] = 6
        part["height"] = 3
        part["thickness"] = 12
        part["name"] = "toy_bubble_wand_33_mm_diameter_double"
        types.append(part)

        part = {}
        part["width"] = 5
        part["height"] = 5
        part["thickness"] = 12
        part["name"] = "toy_bubble_wand_33_mm_diameter_quadruple"
        types.append(part)

        for par in types:
            wid = par["width"]
            hei = par["height"]
            thi = par["thickness"]
            nam = par["name"]
            part = copy.deepcopy(part_default)
            p3 = copy.deepcopy(kwargs)
            p3["width"] = wid
            p3["height"] = hei
            p3["thickness"] = thi
            #p3["extra"] = ""
            part["kwargs"] = p3
            nam = nam
            part["name"] = nam
            if oomp_mode == "oobb":
                p3["oomp_size"] = nam
            parts.append(part)

    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    #generate navigation
    if navigation:
        sort = []
        #sort.append("extra")
        sort.append("name")
        sort.append("width")
        sort.append("height")
        sort.append("thickness")
        
        scad_help.generate_navigation(sort = sort)


def get_base(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "perimeter"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    #oobb_base.append_full(thing,**p3)

    #add cylinder in middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["diameter"] = 30/2
    p3["depth"] = depth
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[1] += 0
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_toy_bubble_wand_33_mm_diameter(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    poss = []
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "corner"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add cylinder in middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["radius"] = 30/2
    p3["depth"] = depth    
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    p3["pos"] = pos1
    oobb_base.append_full(thing,**p3)

    #add screw
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m5_screw_wood"
    dep = 7
    p3["depth"] = dep
    p3["clearance"] = "top"
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    pos1[1] += ((height * 15)-1)/2 - dep
    p3["pos"] = pos1
    rot1 = copy.deepcopy(rot)
    rot1[0] += 90
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)

    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)
    

def get_toy_bubble_wand_33_mm_diameter_double(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    shift_base = 7*15

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 0
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += shift_base
    poss.append(pos12)

    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "corner"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #add cylinder in middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["radius"] = 30/2
    p3["depth"] = depth    
    p3["m"] = "#"
    shift_x = 22.5
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += shift_x
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += -shift_x
    poss.append(pos12)
    poss13 = copy.deepcopy(pos1)
    poss13[0] += shift_x + shift_base
    poss13[2] += 2
    poss.append(poss13)
    poss14 = copy.deepcopy(pos1)
    poss14[0] += -shift_x + shift_base 
    poss14[2] += 2
    poss.append(poss14)
    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #add screw rings
    if False:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["diameter_name"] = "m3_screw_wood"
        dep = 7
        p3["depth"] = dep
        p3["clearance"] = "top"
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth/2
        pos1[1] += ((height * 15)-1)/2 - dep
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_x
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -shift_x
        poss.append(pos12)
        p3["pos"] = poss
        rot1 = copy.deepcopy(rot)
        rot1[0] += 90
        p3["rot"] = rot1
        oobb_base.append_full(thing,**p3)

    #add screw base
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m5_screw_wood"
    dep = (height * 15)-1
    p3["depth"] = dep
    p3["clearance"] = "top"
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    pos1[1] += ((height * 15)-1)/2 - dep
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += shift_base
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += 0
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    rot1[0] += 90
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)

def get_toy_bubble_wand_33_mm_diameter_quadruple(thing, **kwargs):

    prepare_print = kwargs.get("prepare_print", False)
    width = kwargs.get("width", 1)
    height = kwargs.get("height", 1)
    depth = kwargs.get("thickness", 3)                    
    rot = kwargs.get("rot", [0, 0, 0])
    pos = kwargs.get("pos", [0, 0, 0])
    extra = kwargs.get("extra", "")
    
    shift_base = 7*15

    #add plate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "positive"
    p3["shape"] = f"oobb_plate"    
    p3["depth"] = depth
    #p3["holes"] = True         uncomment to include default holes
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += 0
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += shift_base
    poss.append(pos12)

    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)
    
    #add holes seperate
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "p"
    p3["shape"] = f"oobb_holes"
    p3["both_holes"] = True  
    p3["depth"] = depth
    p3["holes"] = "corner"
    #p3["m"] = "#"
    pos1 = copy.deepcopy(pos)         
    p3["pos"] = poss
    #oobb_base.append_full(thing,**p3)

    #add cylinder in middle
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_cylinder"
    p3["radius"] = 30/2
    p3["depth"] = depth    
    p3["m"] = "#"
    shift_x = 18
    shift_y = 18
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += shift_x
    pos11[1] += shift_y
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += -shift_x
    pos12[1] += shift_y
    poss.append(pos12)
    poss13 = copy.deepcopy(pos1)
    poss13[0] += shift_x
    poss13[1] += -shift_y
    poss.append(poss13)
    poss14 = copy.deepcopy(pos1)
    poss14[0] += -shift_x
    poss14[1] += -shift_y
    poss.append(poss14)

    p3["pos"] = poss
    oobb_base.append_full(thing,**p3)

    #add screw rings
    if False:
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "negative"
        p3["shape"] = f"oobb_screw_countersunk"
        p3["diameter_name"] = "m3_screw_wood"
        dep = 7
        p3["depth"] = dep
        p3["clearance"] = "top"
        p3["m"] = "#"
        pos1 = copy.deepcopy(pos)
        pos1[2] += depth/2
        pos1[1] += ((height * 15)-1)/2 - dep
        poss = []
        pos11 = copy.deepcopy(pos1)
        pos11[0] += shift_x
        poss.append(pos11)
        pos12 = copy.deepcopy(pos1)
        pos12[0] += -shift_x
        poss.append(pos12)
        p3["pos"] = poss
        rot1 = copy.deepcopy(rot)
        rot1[0] += 90
        p3["rot"] = rot1
        oobb_base.append_full(thing,**p3)

    #add screw base
    p3 = copy.deepcopy(kwargs)
    p3["type"] = "negative"
    p3["shape"] = f"oobb_screw_countersunk"
    p3["radius_name"] = "m5_screw_wood"
    dep = (height * 15)-1
    p3["depth"] = dep
    p3["clearance"] = "top"
    p3["m"] = "#"
    pos1 = copy.deepcopy(pos)
    pos1[2] += depth/2
    pos1[1] += ((height * 15)-1)/2 - dep
    poss = []
    pos11 = copy.deepcopy(pos1)
    pos11[0] += shift_base
    poss.append(pos11)
    pos12 = copy.deepcopy(pos1)
    pos12[0] += 0
    poss.append(pos12)
    p3["pos"] = poss
    rot1 = copy.deepcopy(rot)
    rot1[0] += 90
    p3["rot"] = rot1
    oobb_base.append_full(thing,**p3)


    if prepare_print:
        #put into a rotation object
        components_second = copy.deepcopy(thing["components"])
        return_value_2 = {}
        return_value_2["type"]  = "rotation"
        return_value_2["typetype"]  = "p"
        pos1 = copy.deepcopy(pos)
        pos1[0] += 50
        return_value_2["pos"] = pos1
        return_value_2["rot"] = [180,0,0]
        return_value_2["objects"] = components_second
        
        thing["components"].append(return_value_2)

    
        #add slice # top
        p3 = copy.deepcopy(kwargs)
        p3["type"] = "n"
        p3["shape"] = f"oobb_slice"
        pos1 = copy.deepcopy(pos)
        pos1[0] += -500/2
        pos1[1] += 0
        pos1[2] += -500/2        
        p3["pos"] = pos1
        #p3["m"] = "#"
        oobb_base.append_full(thing,**p3)


if __name__ == '__main__':
    kwargs = {}
    main(**kwargs)