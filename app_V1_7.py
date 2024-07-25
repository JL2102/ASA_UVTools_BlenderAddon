bl_info = {
    "name": "JL's ASA Mesh Preparation and Toolkit",
    "author": "JL",
    "version": (1, 6),
    "blender": (3, 6, 0), # Do not change, unless BPY documentation updates
    "location": "View",
    "description": "Performs a series of operations on a specified mesh",
    "category": "UV",
}

import bpy

class Utils:
    @staticmethod
    def show_popup_message(message, title="Error", icon='ERROR'):
        def draw(self, context):
            self.layout.label(text=message)
        bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

    @staticmethod
    def get_mesh(mesh_name):
        mesh = bpy.data.objects.get(mesh_name)
        if not mesh:
            Utils.show_popup_message(f"Object '{mesh_name}' not found.")
        elif mesh.type != 'MESH':
            Utils.show_popup_message(f"'{mesh_name}' is not a mesh.")
            mesh = None
        return mesh

    @staticmethod
    def select_and_activate_object(obj):
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj


class MeshOperations:
    @staticmethod
    def rename_initial_uv(mesh_name):
        mesh = Utils.get_mesh(mesh_name)
        if mesh and mesh.data.uv_layers:
            mesh.data.uv_layers[0].name = "DiffuseUV"
        else:
            Utils.show_popup_message(f"No UV layers found on '{mesh_name}'.")

    @staticmethod
    def clear_parent_and_delete_bones(mesh_name):
        mesh = Utils.get_mesh(mesh_name)
        if mesh:
            Utils.select_and_activate_object(mesh)
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            for obj in bpy.data.objects:
                if obj.type == 'ARMATURE' and obj.name != 'ROOT_JNT_SKL':
                    if obj.name in bpy.context.view_layer.objects:
                        Utils.select_and_activate_object(obj)
                        bpy.ops.object.delete()
            print("Deleted all armatures except 'ROOT_JNT_SKL'.")

    @staticmethod
    def manage_uvs(mesh_name):
        mesh = Utils.get_mesh(mesh_name)
        if mesh:
            Utils.select_and_activate_object(mesh)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            for uv in mesh.data.uv_layers:
                if uv.name != 'DiffuseUV':
                    mesh.data.uv_layers.remove(uv)
            bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def transfer_mesh_data(source_mesh, target_mesh):
        source = Utils.get_mesh(source_mesh)
        target = Utils.get_mesh(target_mesh)
        if source and target:
            Utils.select_and_activate_object(target)
            bpy.context.view_layer.objects.active = source
            bpy.ops.object.data_transfer(
                use_reverse_transfer=False, use_freeze=False, data_type='UV', use_create=True,
                loop_mapping='POLYINTERP_NEAREST', poly_mapping='NORMAL',
                use_auto_transform=False, use_object_transform=True,
                use_max_distance=False, max_distance=1.0, ray_radius=0.0, islands_precision=1.0,
                layers_select_src='LightMapUV', layers_select_dst='NAME', mix_mode='REPLACE', mix_factor=1.0
            )

    @staticmethod
    def set_armature(mesh_name, armature_name='ROOT_JNT_SKL'):
        mesh = Utils.get_mesh(mesh_name)
        armature = bpy.data.objects.get(armature_name)
        if not armature:
            Utils.show_popup_message(f"Armature object '{armature_name}' not found.")
            return
        if armature.name != 'ROOT_JNT_SKL':
            armature.name = 'ROOT_JNT_SKL'
        if mesh:
            armature_mod = next((mod for mod in mesh.modifiers if mod.type == 'ARMATURE'), None)
            if armature_mod:
                armature_mod.object = armature
            else:
                armature_mod = mesh.modifiers.new(name="Armature", type='ARMATURE')
                armature_mod.object = armature

    @staticmethod
    def clean_up_uvs(mesh_name):
        mesh = Utils.get_mesh(mesh_name)
        if mesh:
            Utils.select_and_activate_object(mesh)
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            for uv in mesh.data.uv_layers:
                if uv.name not in ['DiffuseUV', 'LightMapUV']:
                    mesh.data.uv_layers.remove(uv)
            bpy.ops.object.mode_set(mode='OBJECT')

    @staticmethod
    def remove_lod_assets():
        lod_names = ["Human_Male_TPV_LOD1", "Human_Male_TPV_LOD2", "Human_Male_TPV_LOD3", "Human_Male_TPV_LOD4"]
        for name in lod_names:
            obj = bpy.data.objects.get(name)
            if obj:
                bpy.data.objects.remove(obj, do_unlink=True)
                print(f"Removed {name}")

    @staticmethod
    def update_mesh_enum(self, context):
        meshes = [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'MESH']
        return meshes

# Yes these show up as errors, but they are not. The functions are being called by the EnumProperty.
class MeshToolsProperties(bpy.types.PropertyGroup):
    enable_operations: bpy.props.BoolProperty(
        name="Enable Operations",
        default=True,
        description="Enable or disable operations"
    )
    enable_remove_lods: bpy.props.BoolProperty(
        name="Remove LOD Assets",
        default=False
    )
    enable_rename_uv: bpy.props.BoolProperty(
        name="Rename Initial UV",
        default=False
    )
    enable_clear_bones: bpy.props.BoolProperty(
        name="Clear Bones",
        default=True
    )
    enable_manage_uvs: bpy.props.BoolProperty(
        name="Manage UVs",
        default=True
    )
    enable_transfer_data: bpy.props.BoolProperty(
        name="Transfer Data",
        default=True
    )
    enable_set_armature: bpy.props.BoolProperty(
        name="Set Armature",
        default=True
    )
    enable_clean_up_uvs: bpy.props.BoolProperty(
        name="Clean Up UVs",
        default=True
    )
    mesh_enum: bpy.props.EnumProperty(
        name="Select Mesh",
        description="Select a mesh from the scene",
        items=MeshOperations.update_mesh_enum,
    )


class MESH_OT_CompleteOperation(bpy.types.Operator):
    bl_idname = "mesh.complete_operation"
    bl_label = "Execute Mesh Operations"
    
    def execute(self, context):
        props = context.scene.mesh_tools
        if props.enable_remove_lods:
            MeshOperations.remove_lod_assets()

        # Ensure Human_Male_TPV is imported
        if not bpy.data.objects.get("Human_Male_TPV_LodGroup"):
            self.report({'ERROR'}, "Please Import ASA's Human_Male_TPV FBX into the project.")
            return {'CANCELLED'}
        
        # Esure mesh name is selected
        mesh_name = props.mesh_enum
        if not mesh_name:
            self.report({'ERROR'}, "No mesh name selected.")
            return {'CANCELLED'}
        
        # Execute operations
        if props.enable_rename_uv:
            MeshOperations.rename_initial_uv(mesh_name)
        if props.enable_clear_bones:
            MeshOperations.clear_parent_and_delete_bones(mesh_name)
        if props.enable_manage_uvs:
            MeshOperations.manage_uvs(mesh_name)
        if props.enable_transfer_data:
            MeshOperations.transfer_mesh_data("Human_Male_TPV_LOD0", mesh_name)
        if props.enable_set_armature:
            MeshOperations.set_armature(mesh_name)
        if props.enable_clean_up_uvs:
            MeshOperations.clean_up_uvs(mesh_name)
        return {'FINISHED'}


class MESH_OT_ShowHelp(bpy.types.Operator):
    bl_idname = "mesh.show_help"
    bl_label = "Show Help"
    bl_options = {'REGISTER'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self, width=550)
    
    # Info on Mesh Operations
    def draw(self, context):
        layout = self.layout
        layout.label(text="Help - Mesh Operations", icon='INFO')
        layout.label(text="Remove LOD Assets: Ensures Human Male TPV model only has LOD0")
        layout.label(text="Rename Initial UV: Renames the initial UV layer to 'DiffuseUV'.")
        layout.label(text="Clear Bones: Clears parent and deletes all armatures except 'ROOT_JNT_SKL'.")
        layout.label(text="Manage UVs: Deletes all UV layers except 'DiffuseUV'. to ensure only wanted UV layers exist.")
        layout.label(text="Transfer Data: Transfers UV data from 'Human_Male_TPV_LOD0' to selected mesh.")
        layout.label(text="Set Armature: Sets the armature to 'ROOT_JNT_SKL'.")
        layout.label(text="Clean Up UVs: Deletes all UV layers except 'DiffuseUV' and 'LightMapUV'. Cleans up temporary files")

    def execute(self, context):
        return {'FINISHED'}


class MESH_PT_ControlPanel(bpy.types.Panel):
    bl_label = "Mesh Preparation Tools"
    bl_idname = "MESH_PT_control_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.mesh_tools
        
        layout.label(text="Configure and run mesh preparation operations:")
        layout.prop(props, "mesh_enum", text="Select Mesh")
        
        row = layout.row()
        row.operator(MESH_OT_ShowHelp.bl_idname, text="", icon='INFO')
        
        # Enable Operations dropdown
        box = layout.box()
        box.prop(props, "enable_operations", icon="TRIA_DOWN" if props.enable_operations else "TRIA_RIGHT", emboss=False)
        
        if props.enable_operations:
            col = box.column(align=True)
            col.prop(props, "enable_remove_lods", text="Remove LOD Assets")
            col.prop(props, "enable_rename_uv", text="Rename Initial UV")
            col.prop(props, "enable_clear_bones", text="Clear Bones")
            col.prop(props, "enable_manage_uvs", text="Manage UVs")
            col.prop(props, "enable_transfer_data", text="Transfer Data")
            col.prop(props, "enable_set_armature", text="Set Armature")
            col.prop(props, "enable_clean_up_uvs", text="Clean Up UVs")
        
        layout.operator(MESH_OT_CompleteOperation.bl_idname)


def register():
    bpy.utils.register_class(MeshToolsProperties)
    bpy.utils.register_class(MESH_OT_CompleteOperation)
    bpy.utils.register_class(MESH_OT_ShowHelp)
    bpy.utils.register_class(MESH_PT_ControlPanel)
    bpy.types.Scene.mesh_tools = bpy.props.PointerProperty(type=MeshToolsProperties)

def unregister():
    bpy.utils.unregister_class(MeshToolsProperties)
    bpy.utils.unregister_class(MESH_OT_CompleteOperation)
    bpy.utils.unregister_class(MESH_OT_ShowHelp)
    bpy.utils.unregister_class(MESH_PT_ControlPanel)
    del bpy.types.Scene.mesh_tools

if __name__ == "__main__":
    register()
