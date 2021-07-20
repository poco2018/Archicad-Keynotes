#include	"AdditionalJSONCommands.hpp"
#include	"ObjectState.hpp"
#include	"FileSystem.hpp"
#include    "AddOnMain.hpp"

constexpr const char* AdditionalJSONCommandsNamespace = "AdditionalJSONCommands";


static GS::HashTable<GS::UniString, API_Guid> GetPublisherSetNameGuidTable ()
{
	GS::HashTable<GS::UniString, API_Guid> table;

	Int32 numberOfPublisherSets = 0;
	ACAPI_Navigator (APINavigator_GetNavigatorSetNumID, &numberOfPublisherSets);

	API_NavigatorSet set = {};
	for (Int32 ii = 0; ii < numberOfPublisherSets; ++ii) {
		set.mapId = API_PublisherSets;
		if (ACAPI_Navigator (APINavigator_GetNavigatorSetID, &set, &ii) == NoError) {
			table.Add (set.name, set.rootGuid);
		}
	}

	return table;
}


static GS::Optional<IO::Location>	GetApplicationLocation ()
{
	IO::Location applicationFileLocation;

	GSErrCode error = IO::fileSystem.GetSpecialLocation (IO::FileSystem::ApplicationFile, &applicationFileLocation);
	if (error != NoError) {
		return GS::NoValue;
	}

	return applicationFileLocation;
}


constexpr const char* ErrorResponseField = "error";
constexpr const char* ErrorCodeResponseField = "code";
constexpr const char* ErrorMessageResponseField = "message";


static GS::ObjectState CreateErrorResponse(APIErrCodes errorCode, const char* errorMessage)
{
	GS::ObjectState error;
	error.Add(ErrorCodeResponseField, errorCode);
	error.Add(ErrorMessageResponseField, errorMessage);
	return GS::ObjectState(ErrorResponseField, error);
}

// --- AdditionalJSONCommand ----------------------------------------------------------------------------------

GS::String AdditionalJSONCommand::GetNamespace() const
{
	return AdditionalJSONCommandsNamespace;
}


GS::Optional<GS::UniString> AdditionalJSONCommand::GetSchemaDefinitions() const
{
	return {};
}


GS::Optional<GS::UniString> AdditionalJSONCommand::GetInputParametersSchema() const
{
	return {};
}


GS::Optional<GS::UniString> AdditionalJSONCommand::GetResponseSchema() const
{
	return GS::UniString::Printf(R"({
	"type": "object",
	"properties": {
		"%s": {
			"$ref": "APITypes.json#/definitions/Error"
		}
	},
	"additionalProperties": false,
	"required": []
})",
ErrorResponseField);
}


void AdditionalJSONCommand::OnResponseValidationFailed(const GS::ObjectState& /*response*/) const
{
	ACAPI_WriteReport(" JSON Validation Failed", true);
}

// ----------  KeyNote Command  -------------------------------

GS::String KeyNoteCommand::GetName() const
{
	
	return "KeyNote";
}

constexpr const char* SymbolShapeParameterField = "Symbol Shape";
constexpr const char* TextPenParameterField = "Text Pen";
constexpr const char* FontTypeParameterField = "Font Type";
constexpr const char* FontSizeParameterField = "Font Size";
constexpr const char* FontstyleBoldParameterField = "Font Style Bold";
constexpr const char* FontStyleItalicParameterField = "Font Style Italic";
constexpr const char* FontStyleUnderLineParameterField = "Font Style UnderLine";
constexpr const char* ContourPenParameterField = "Contour Pen";
constexpr const char* FillTypeParameterField = "Fill Type";
constexpr const char* FillPenParameterField = "Fill Pen";
constexpr const char* FillBackGroundPenParameterField = "Fill BackGround Pen";
constexpr const char* TextOrientationParameterField = "typeTextRotation";
constexpr const char* ClassificationParameterField = "Classification";
constexpr const char* NoteRootField = "Class_Root";
constexpr const char* CircleDiameterParameterField = "CircleDiameter";
constexpr const char* DisciplineParameterField = "Discipline";
constexpr const char* TextParameterField = "txt";
constexpr const char* NoteParameterField = "note";




GS::Optional<GS::UniString> KeyNoteCommand::GetInputParametersSchema() const
{
	

	return GS::UniString::Printf(R"({
	"type": "object",
	"properties": {
		"%s": {
			"type": "string",
			"description": "The name of the Library Shape",
			"minLength": 1
		},
		"%s": {
			"type": "integer",
			"description": "Text Pen Number.",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "The name of the Font",
			"minLength": 1
		},
		"%s": {
			"type": "number",
			"description": "Font Size in mm",
			"minLength": 1
		},
		"%s": {
			"type": "boolean",
			"description": "Bold Toggle",
			"minLength": 1
		},
		"%s": {
			"type": "boolean",
			"description": "Italic Toggle",
			"minLength": 1
		},
		"%s": {
			"type": "boolean",
			"description": "UnderLine Toggle",
			"minLength": 1
		},
		"%s": {
			"type": "integer",
			"description": "Contour Pen Number.",
			"minLength": 1
		},
		"%s": {
			"type": "integer",
			"description": "Fill Type Pen Number",
			"minLength": 1
		},
		"%s": {
			"type": "integer",
			"description": "Fill Pen Number",
			"minLength": 1
		},
		"%s": {
			"type": "integer",
			"description": "Fill BackGround Pen Number",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "Type Rotation",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "Classification",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "Discipline",
			"minLength": 1
		},
		"%s": {
			"type": "number",
			"description": "Diameter",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "txt",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "note",
			"minLength": 1
		},
		"%s": {
			"type": "string",
			"description": "keynote class",
			"minLength": 1
		}
	},
"additionalProperties": false,
	"required": [
		"%s"
	]
})",
SymbolShapeParameterField, TextPenParameterField, FontTypeParameterField,FontSizeParameterField,
FontstyleBoldParameterField, FontStyleItalicParameterField, FontStyleUnderLineParameterField, 
ContourPenParameterField, FillTypeParameterField, FillPenParameterField,FillBackGroundPenParameterField,
TextOrientationParameterField, ClassificationParameterField, DisciplineParameterField,
CircleDiameterParameterField, TextParameterField, NoteParameterField, NoteRootField,
SymbolShapeParameterField
);
	// Never gets here because of above return
	
}

keyParams keysettings;
GS::ObjectState	KeyNoteCommand::Execute(const GS::ObjectState& parameters, GS::ProcessControl& /*processControl*/) const
{
	
	// transfer style settings
	parameters.Get(SymbolShapeParameterField,keysettings.shape);
	parameters.Get(TextPenParameterField, keysettings.tpen);
	parameters.Get(FontTypeParameterField, keysettings.fontType);
	parameters.Get(FontSizeParameterField, keysettings.fsz);
	parameters.Get(FontstyleBoldParameterField, keysettings.gs_text_style_bold);
	parameters.Get(FontStyleItalicParameterField, keysettings.gs_text_style_italic);
	parameters.Get(FontStyleUnderLineParameterField, keysettings.gs_text_style_underline);
	parameters.Get(ContourPenParameterField, keysettings.gs_cont_pen);
	parameters.Get(FillTypeParameterField, keysettings.gs_fill_type);
	parameters.Get(FillPenParameterField, keysettings.gs_fill_pen);
	parameters.Get(FillBackGroundPenParameterField, keysettings.gs_back_pen);
	parameters.Get(TextOrientationParameterField, keysettings.typeTextRotation);
	parameters.Get(ClassificationParameterField, keysettings.classification);
	parameters.Get(DisciplineParameterField, keysettings.discipline);
	parameters.Get(CircleDiameterParameterField, keysettings.shapeDiameter);
	parameters.Get(TextParameterField, keysettings.txt);
	parameters.Get(NoteParameterField, keysettings.note);
	parameters.Get(NoteRootField, keysettings.class_root);
	

	// end of transfer section
    // Activate Keynote Code
	
	GSErrCode err =  Do_PlaceKeySymbol(keysettings);

	if (err != NoError) {
		return GS::ObjectState(ErrorMessageResponseField, "Keynote failed. Check parameters");
	}

	return {};
}




// ----------  End KeyNote Command  -------------------------------