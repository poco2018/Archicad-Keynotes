#include "APIEnvir.h"
#include "ACAPinc.h"
#include "Resourceids.hpp"
#include "AdditionalJSONCommands.hpp"
#include "AddOnMain.hpp"
#include "resource.h"
#include "DGModule.hpp"
#include "APICommon.h"
#include  <string>
#include <uchar_t.hpp>
#include <typeinfo>

static const GSResID AddOnInfoID			= ID_ADDON_INFO;
	static const Int32 AddOnNameID			= 1;
	static const Int32 AddOnDescriptionID	= 2;

static const short AddOnMenuID				= ID_ADDON_MENU;
	static const Int32 AddOnCommandID		= 1;
	GS::Array<API_Guid> arr;
	

	GS::ErrCode	Do_CreateLine(API_Guid guid,API_Coord* cc)
	{
		API_Coord			c;
		API_GetLineType		clickInfo;
		API_Element			element;
		GSErrCode			err;

		// input the coordinates
		BNZeroMemory(&clickInfo, sizeof(API_GetLineType));
		if (!ClickAPoint("Click the line start point", &c))
			return NoError;

		CHCopyC("Click the line Middle point", clickInfo.prompt);

		clickInfo.startCoord.x = c.x;
		clickInfo.startCoord.y = c.y;
		err = ACAPI_Interface(APIIo_GetLineID, &clickInfo, nullptr);

		BNZeroMemory(&element, sizeof(API_Element));
		element.header.typeID = API_LineID;
		ACAPI_Element_GetDefaults(&element, nullptr);
		if (err != NoError) {
			ErrorBeep("ACAPI_Element_GetDefaults (Line)", err);
			return NoError;
		}

		element.header.renovationStatus = API_DemolishedStatus;
		element.line.begC.x = clickInfo.startCoord.x;
		element.line.begC.y = clickInfo.startCoord.y;
		element.line.endC.x = clickInfo.pos.x;
		element.line.endC.y = clickInfo.pos.y;
		element.line.arrowData.begArrow = true;
		element.line.arrowData.arrowSize = 1;
		element.line.arrowData.arrowType = APIArr_FullArrow30;
		element.line.arrowData.arrowPen = 6;
		element.line.ltypeInd = 1;
		element.line.linePen.penIndex = 33;
		arr.Clear();
		
		err = ACAPI_CallUndoableCommand("Leader line Test API Function",
			[&]() -> GSErrCode {
			err = ACAPI_Element_Create(&element, nullptr);
			arr.Push(element.line.head.guid);
			return err; });

		CHCopyC("Click the line Finish point", clickInfo.prompt);
		clickInfo.startCoord.x = clickInfo.pos.x;
		clickInfo.startCoord.y = clickInfo.pos.y;
		err = ACAPI_Interface(APIIo_GetLineID, &clickInfo, nullptr);
		if (err != NoError) {
			ErrorBeep("APIIo_GetLineID", err);
			return NoError;
		}

		// real work
		BNZeroMemory(&element, sizeof(API_Element));
		element.header.typeID = API_LineID;
		ACAPI_Element_GetDefaults(&element, nullptr);
		if (err != NoError) {
			ErrorBeep("ACAPI_Element_GetDefaults (Line)", err);
			return NoError;
		}

		element.header.renovationStatus = API_DemolishedStatus;
		element.line.begC.x = clickInfo.startCoord.x;
		element.line.begC.y = clickInfo.startCoord.y;
		element.line.endC.x = clickInfo.pos.x;
		element.line.endC.y = clickInfo.pos.y;
		element.line.arrowData.begArrow = false;
		element.line.arrowData.arrowSize = .5;
		element.line.arrowData.arrowType = APIArr_OpenArrow30;
		element.line.arrowData.arrowPen= 6;
		element.line.ltypeInd = 1;
		element.line.linePen.penIndex = 33;
		err =ACAPI_CallUndoableCommand("End Leader Test API Function",
			[&]() -> GSErrCode {
			err = ACAPI_Element_Create(&element, nullptr);
			arr.Push(element.line.head.guid);
			return err; });
		if (err != NoError) {
			ErrorBeep("ACAPI_Element_Create (Line)", err);
			ACAPI_WriteReport("Create Error = %s", true, ErrID_To_Name(err));
			return err;
		}
		//Added code here
		
		guid = element.header.guid;		// store it for later use
		ACAPI_KeepInMemory(true);
		
		cc->x = clickInfo.pos.x + .02;
		cc->y = clickInfo.pos.y;
		// End of Added Code here
		//guid = element.header.guid;		// store it for later use

		//ACAPI_KeepInMemory(true);

		return NoError;
	}		// Do_CreateLine

	 GS::ErrCode Do_ChangeLibPart(API_Coord c,  keyParams keys) {
		
		GS::UniString name("Keynote Symbol_3");
		API_LibPart libPart;
		API_Element          element;
		API_ElementMemo      memo;
		API_AddParType   **addPars = nullptr;
		//API_Guid nn;
		double a, b;
		Int32 addParNum;
		GS::ErrCode err;
		
		BNZeroMemory(&libPart, sizeof(API_LibPart));
		BNZeroMemory(&element, sizeof(API_Element));
		BNZeroMemory(&memo, sizeof(API_ElementMemo));

		GS::ucscpy(libPart.docu_UName, name.ToUStr());
		
		err = ACAPI_LibPart_Search(&libPart, false);
		if (err ){
			ACAPI_WriteReport("Did not find library part",true);
			return err;
		}
		if (libPart.location != nullptr)
			delete libPart.location;
		element.header.typeID = API_ObjectID; //ElementTypeID
		element.header.variationID = APIVarId_Object;
		element.object.libInd = libPart.index; //library part index
		element.header.hasMemo = true;
		err = ACAPI_Element_GetDefaults(&element, &memo);
		element.header.hasMemo = true;
		element.header.drwIndex = 120;
		API_StoryInfo storyInfo;
		BNZeroMemory(&storyInfo, sizeof(API_StoryInfo));
		err = ACAPI_Environment(APIEnv_GetStorySettingsID, &storyInfo, nullptr);
		element.object.libInd = libPart.index; //library part index8;
		element.header.floorInd = storyInfo.actStory;
		element.object.level = 0; //height from the floor
		element.object.pos.x = c.x + .25; //End of Arrow
		element.object.pos.y = c.y;
		element.object.angle = 1; //element angle
		BMKillHandle((GSHandle *)&storyInfo.data);
		
		GS::Guid buf("0DF8E541 - 68EB - 4102 - 8886 - C144F74770E0");// keynote_2
		//GS::Guid buf("0DF8E541 - 68EB - 4102 - 8886 - C144F74770E0");
		element.object.head.guid = GSGuid2APIGuid(buf);
		err = ACAPI_LibPart_GetParams(libPart.index, &a, &b, &addParNum, &addPars);
		UInt32 totalParams = BMGetHandleSize((GSConstHandle)addPars) / (UInt32)sizeof(API_AddParType);
		// totalParams redundant but retain for future use
		for (unsigned int i = 0; i < totalParams; i++) {


			if (CHEqualASCII("shape", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.shape.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("tpen", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.tpen;
			}
			if (CHEqualASCII("fontType", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.fontType.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("fsz", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.fsz;
			}
			if (CHEqualASCII("gs_text_style_bold", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_text_style_bold;
			}
			if (CHEqualASCII("gs_text_style_italic", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_text_style_italic;
			}
			if (CHEqualASCII("gs_text_style_underline", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_text_style_underline;
			}
			if (CHEqualASCII("ga_cont_pen", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_cont_pen;
			}
			if (CHEqualASCII("gs_fill_type", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_fill_type;
			}
			if (CHEqualASCII("gs_fill_pen", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_fill_pen;
			}
			if (CHEqualASCII("gs_back_pen", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.gs_back_pen;
			}
			if (CHEqualASCII("typeTextRotation", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.txt.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("circleRadius", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.shapeRadius;
			}
			if (CHEqualASCII("circleDiameter", (*addPars)[i].name, CS_CaseInsensitive)) {
				(*addPars)[i].value.real = keys.shapeDiameter;
			}
			if (CHEqualASCII("txt", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.txt.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("note", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.note.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("discipline", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.discipline.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("classification", (*addPars)[i].name, CS_CaseInsensitive)) {
				GS::ucsncpy((*addPars)[i].value.uStr, keys.classification.ToUStr().Get(), API_UAddParStrLen - 1);
			}
			if (CHEqualASCII("typeTextRotation", (*addPars)[i].name, CS_CaseInsensitive)) {
				//ACAPI_WriteReport("inside Rotation %s", true, keys.typeTextRotation.ToCStr().Get());
				(*addPars)[i].value.real = 2;
				//GS::ucsncpy((*addPars)[i].value.uStr, keys.typeTextRotation.ToUStr().Get(), API_UAddParStrLen - 1);
			}
		}
		memo.params = addPars;
		err = ACAPI_CallUndoableCommand("Place Keynote Function",
			[&]() -> GSErrCode {
			err = ACAPI_Element_Create(&element, &memo);
			// added here
			arr.Push(element.header.guid);
			
			err = ACAPI_Element_Tool(arr, APITool_BringToFront,nullptr);
			// added here end

			return err;
		});
		if (err)
			ACAPI_WriteReport("Create Error 11 %s ", true, ErrID_To_Name(err));
		return NOERROR;
	}
	
	GS::ErrCode Do_PlaceKeySymbol( keyParams abc) {
		//ACAPI_WriteReport("inside placekeysymbol %s", true, abc.shape.ToCStr().Get());
		API_Coord c;
		GS::ErrCode	err;
		c.x = 0;
		c.y = 0;
		err = Do_CreateLine(APINULLGuid, &c);
		//ACAPI_WriteReport("inside placekeysymbol", true);
		Do_ChangeLibPart(c,abc);
		return NoError;
	}

	static void	ReplaceEmptyTextWithPredefined(API_ElementMemo& memo)
	{
		const char* predefinedContent = "Default text was empty.";

		if (memo.textContent == nullptr || Strlen32(*memo.textContent) < 2) {
			BMhKill(&memo.textContent);
			memo.textContent = BMhAllClear(Strlen32(predefinedContent) + 1);
			strcpy(*memo.textContent, predefinedContent);
			(*memo.paragraphs)[0].run[0].range = Strlen32(predefinedContent);
		}
	}

	GS::ErrCode	Do_CreateLabel(void)
	{
		API_Coord c;
		if (!ClickAPoint("Click label reference point", &c))
			return NoError;

		GSErrCode			err;
		API_Element			element;
		API_ElementMemo		memo;

		BNZeroMemory(&element, sizeof(API_Element));
		element.header.typeID = API_LabelID;

		err = ACAPI_Element_GetDefaults(&element, &memo);
		if (err != NoError) {
			ErrorBeep("ACAPI_Element_GetDefaults", err);
			ACAPI_WriteReport("Defaults Error - %s", true, ErrID_To_Name(err));
			return err;
		}
		else
			ACAPI_WriteReport("After get Defaults", true);

		element.label.parent = APINULLGuid;
		element.label.begC = c;
		element.label.midC.x = c.x + 1.0;
		element.label.midC.y = c.y + 0.5;
		element.label.endC.x = c.x + 3.0;
		element.label.endC.y = c.y + 0.5;

		if (element.label.labelClass == APILblClass_Text) {
			ReplaceEmptyTextWithPredefined(memo);
			element.label.u.text.nonBreaking = true;
		}


		err = ACAPI_Element_Create(&element, &memo);
		if (err != NoError){
			ErrorBeep("ACAPI_Element_Create (Label)", err);
			ACAPI_WriteReport("Create Error - %s", true, ErrID_To_Name(err));
		}
		ACAPI_WriteReport("After Create Label", true);
		ACAPI_DisposeElemMemoHdls(&memo);
		return NoError;
	}		// Do_CreateLabel
	