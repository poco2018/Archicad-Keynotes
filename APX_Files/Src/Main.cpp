// *****************************************************************************
// Contact person:	Tibor Lor�ntfy (tlorantfy@graphisoft.com)
// *****************************************************************************

#include	"APIEnvir.h"
#include	"ACAPinc.h"		// also includes APIdefs.h
#include    "AddOnMain.hpp"
#include    "Resourceids.hpp"
#include	"AdditionalJSONCommands.hpp"
#include    "APICommon.h"


// =============================================================================
//
// Required functions
//
// =============================================================================

// -----------------------------------------------------------------------------
// Dependency definitions
// -----------------------------------------------------------------------------

API_AddonType	__ACDLL_CALL	CheckEnvironment (API_EnvirParams* envir)
{
	RSGetIndString (&envir->addOnInfo.name, 32000, 1, ACAPI_GetOwnResModule ());
	RSGetIndString (&envir->addOnInfo.description, 32000, 2, ACAPI_GetOwnResModule ());

	return APIAddon_Preload;
	//return APIAddon_Unknown;
}		// CheckEnvironment

static GSErrCode MenuCommandHandler(const API_MenuParams* menuParams)
{
	
	GS::ErrCode err = NoError;
	switch (menuParams->menuItemRef.menuResID) {
	case 32500:
		switch (menuParams->menuItemRef.itemIndex) {

		case 1:
		{
			
			keyParams keysettings;
			GS::ErrCode err = Do_PlaceKeySymbol(keysettings);
			return err;
		}
		break;
		case 2:
		{

			return ACAPI_CallUndoableCommand("Element Test API Function",
				[&]() -> GSErrCode {
				//err = Do_CreateLabel();
				return NoError;
			});
		}
		
		break;
		}
	}
	return NOERROR;
}
// -----------------------------------------------------------------------------
// Interface definitions
// -----------------------------------------------------------------------------

GSErrCode	__ACDLL_CALL	RegisterInterface (void)
{
	GSErrCode err = ACAPI_Register_Menu(32500, 32600, MenuCode_UserDef, MenuFlag_SeparatorBefore | MenuFlag_SeparatorAfter);
	return NoError;
}		// RegisterInterface


// -----------------------------------------------------------------------------
// Initialize
//		called after the Add-On has been loaded into memory
// -----------------------------------------------------------------------------

GSErrCode __ACENV_CALL	Initialize (void)
{
	GSErrCode err;
	
	err = ACAPI_Install_AddOnCommandHandler(GS::NewOwned<KeyNoteCommand>());
	if (err) {
		ACAPI_WriteReport("CommandHandler Add on Failed- %s", true, ErrID_To_Name(err));
		//return err;
	}
	else
		ACAPI_WriteReport("CommandHandler Add on Success", true);
	
    err = ACAPI_Install_MenuHandler(32500, MenuCommandHandler);
	return err;
}		// Initialize


// -----------------------------------------------------------------------------
// FreeData
//		called when the Add-On is going to be unloaded
// -----------------------------------------------------------------------------

GSErrCode __ACENV_CALL	FreeData (void)
{
	return NoError;
}		// FreeData
