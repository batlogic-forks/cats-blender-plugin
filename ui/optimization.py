import bpy
import globs
import tools.common
import tools.supporter

from ui.main import ToolPanel
from ui.main import layout_split

from tools.register import register_wrap


@register_wrap
class AtlasList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        mat = item.material
        row = layout.row()
        row.prop(mat, 'name', emboss=False, text='', icon_value=layout.icon(mat))
        sub_row = row.row()
        sub_row.scale_x = 0.2
        row.prop(mat, 'add_to_atlas', text='')


@register_wrap
class OptimizePanel(ToolPanel, bpy.types.Panel):
    bl_idname = 'VIEW3D_PT_optimize_v3'
    bl_label = 'Optimization'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align=True)
        row.prop(context.scene, 'optimize_mode', expand=True)

        if context.scene.optimize_mode == 'ATLAS':

            col = box.column(align=True)
            row = col.row(align=True)
            row.scale_y = 0.75
            row.label(text='A greatly improved Atlas Generator.')

            split = col.row(align=True)
            row = split.row(align=True)
            row.scale_y = 0.9
            row.label(text='Made by shotaryia', icon_value=tools.supporter.preview_collections["custom_icons"]["heart1"].icon_id)
            row = split.row(align=True)
            row.alignment = 'RIGHT'
            row.scale_y = 0.9
            row.operator("atlas.help", text="", icon='QUESTION')
            col.separator()

            if len(context.scene.material_list) == 0:
                row = col.row(align=True)
                row.scale_y = 1.2
                row.operator('atlas.gen_mat_list', icon='TRIA_RIGHT')
                col.separator()
            else:
                # row = col.row(align=True)
                # row.scale_y = 0.75
                # row.label(text='Select Materials to Combine:')
                row = col.row(align=True)
                row.template_list('AtlasList', '', context.scene, 'material_list', context.scene, 'material_list_index', rows=8, type='DEFAULT')

                row = layout_split(col, factor=0.8, align=True)
                row.scale_y = 1.2
                row.operator('atlas.gen_mat_list', text='Update Material List', icon='FILE_REFRESH')
                if context.scene.clear_materials:
                    row.operator('atlas.check_mat_list', text='', icon='CHECKBOX_HLT')
                else:
                    row.operator('atlas.check_mat_list', text='', icon='CHECKBOX_DEHLT')

                row.operator('atlas.clear_mat_list', text='', icon='X')
                col.separator()

            row = col.row(align=True)
            row.scale_y = 1.7
            row.operator('atlas.generate', icon='TRIA_RIGHT')

        elif context.scene.optimize_mode == 'MATERIAL':
            col = box.column(align=True)
            row = col.row(align=True)
            row.scale_y = 1.1
            row.operator('combine.mats', icon='MATERIAL')

            row = col.row(align=True)
            row.scale_y = 1.1
            row.operator('one.tex', icon='TEXTURE')
            subcol = row.row(align=True)
            subcol.alignment = 'RIGHT'
            subcol.scale_y = 1.1
            subcol.operator("one.tex_only", text="", icon='X')

            row = col.row(align=True)
            row.scale_y = 1.1
            row.operator('textures.standardize', icon=globs.ICON_SHADING_TEXTURE)

        elif context.scene.optimize_mode == 'BONEMERGING':
            if len(tools.common.get_meshes_objects()) > 1:
                row = box.row(align=True)
                row.prop(context.scene, 'merge_mesh')
            row = box.row(align=True)
            row.prop(context.scene, 'merge_bone')
            row = box.row(align=True)
            row.prop(context.scene, 'merge_ratio')
            row = box.row(align=True)
            col.separator()
            row.operator('refresh.root', icon='FILE_REFRESH')
            row.operator('bone.merge', icon='AUTOMERGE_ON')