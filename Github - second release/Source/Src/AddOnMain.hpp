#if !defined (ADDONMAIN_HPP)
#define ADDONMAIN_HPP
#pragma once

#include	"APIEnvir.h"
#include	"ACAPinc.h"

struct keyParams {
	double shapeDiameter = .23;
	double shapeRadius = .12;
	GS::UniString txt = "G-Gen";
	GS::UniString fontType = "Arial";
	double fsz = 12.8;
	bool gs_text_style_bold = false;
	bool gs_text_style_italic = false;
	bool gs_text_style_underline = false;
	GS::UniString typeTextRotation = "Always Horizontal";
	int tpen = 5;
	int gs_cont_pen = 102;
	int gs_fill_type = -1;
	int gs_fill_pen = 5;
	int gs_back_pen = 6;
	GS::UniString note = "Keynote description will be placed here";
	GS::UniString classification = "classification"; //classification
	GS::UniString shape = "hexagon";
	GS::UniString discipline = "Discipline"; //discipline
	GS::UniString class_root = "Top_Level";  // Classification System
};
//}keysettings;

GS::ErrCode SelectClass(API_Element element, GS::UniString& item);

GS::ErrCode	Do_CreateLine(API_Guid guid, API_Coord cc);

//static GS::ErrCode Do_ChangeLibPart(API_Coord c);

static void	ReplaceEmptyTextWithPredefined(API_ElementMemo& memo);

GS::ErrCode	Do_CreateLabel(void);

 GS::ErrCode Do_PlaceKeySymbol( struct keyParams abc);

 
#endif