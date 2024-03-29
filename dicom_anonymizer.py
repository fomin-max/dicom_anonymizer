import argparse
import glob
import os
import pydicom

# De-identification table
# https://wiki.cancerimagingarchive.net/display/Public/De-identification+Knowledge+Base

DICOM_FIELD_NAMES = ['AccessionNumber',
                     'AcquisitionComments',
                     'AcquisitionContextSeq',
                     'AcquisitionDate',
                     'AcquisitionDatetime',
                     'AcquisitionDeviceProcessingDescription',
                     'AcquisitionProtocolDescription',
                     'AcquisitionTime',
                     'ActualHumanPerformersSequence',
                     'AdditionalPatientHistory',
                     'AdmissionID',
                     'AdmittingDate',
                     'AdmittingDiagnosesCodeSeq',
                     'AdmittingDiagnosesDescription',
                     'AdmittingTime',
                     'Allergies',
                     'Arbitrary',
                     'AuthorObserverSequence',
                     'BlockOwner',
                     'BodyPartExamined',
                     'BranchOfService',
                     'BurnedInAnnotation',
                     'CassetteID',
                     'CommentsOnPPS',
                     'ConcatenationUID',
                     'ConfidentialityPatientData',
                     'ContentCreatorsIdCodeSeq',
                     'ContentCreatorsName',
                     'ContentDate',
                     'ContentSeq',
                     'ContentTime',
                     'ContextGroupExtensionCreatorUID',
                     'ContrastBolusAgent',
                     'ContributionDescription',
                     'CountryOfResidence',
                     'CreatorVersionUID',
                     'CurrentPatientLocation',
                     'CurveDate',
                     'CurveTime',
                     'CustodialOrganizationSeq',
                     'DataSetTrailingPadding',
                     'DateofLastCalibration',
                     'DateofLastDetectorCalibration',
                     'DateOfSecondaryCapture',
                     'DeIdentificationMethod',
                     'DeIdentificationMethodCodeSequence',
                     'DerivationDescription',
                     'DetectorID',
                     'DeviceSerialNumber',
                     'DeviceUID',
                     'DigitalSignaturesSeq',
                     'DigitalSignatureUID',
                     'DimensionOrganizationUID',
                     'DischargeDiagnosisDescription',
                     'DistributionAddress',
                     'DistributionName',
                     'DoseReferenceUID',
                     'EthnicGroup',
                     'FailedSOPInstanceUIDList',
                     'FiducialUID',
                     'FillerOrderNumber',
                     'FrameComments',
                     'FrameOfReferenceUID',
                     'GantryID',
                     'GeneratorID',
                     'GraphicAnnotationSequence',
                     'HumanPerformersName',
                     'HumanPerformersOrganization',
                     'IconImageSequence',
                     'IdentifyingComments',
                     'ImageComments',
                     'ImagePresentationComments',
                     'ImagingServiceRequestComments',
                     'Impressions',
                     'InstanceCreationDate',
                     'InstanceCreatorUID',
                     'InstitutionAddress',
                     'InstitutionalDepartmentName',
                     'InstitutionCodeSequence',
                     'InstitutionName',
                     'InsurancePlanIdentification',
                     'IntendedRecipientsOfResultsIDSequence',
                     'InterpretationApproverSequence',
                     'InterpretationAuthor',
                     'InterpretationDiagnosisDescription',
                     'InterpretationIdIssuer',
                     'InterpretationRecorder',
                     'InterpretationText',
                     'InterpretationTranscriber',
                     'IrradiationEventUID',
                     'IssuerOfAdmissionID',
                     'IssuerOfPatientID',
                     'IssuerOfServiceEpisodeId',
                     'LargePaletteColorLUTUid',
                     'LastMenstrualDate',
                     'LongitudinalTemporalInformationModified',
                     'MAC',
                     'Manufacturer',
                     'ManufacturerModelName',
                     'MedicalAlerts',
                     'MedicalRecordLocator',
                     'MilitaryRank',
                     'ModifiedAttributesSequence',
                     'ModifiedImageDescription',
                     'ModifyingDeviceID',
                     'ModifyingDeviceManufacturer',
                     'NameOfPhysicianReadingStudy',
                     'NamesOfIntendedRecipientsOfResults',
                     'Occupation',
                     'OperatorName',
                     'OperatorsIdentificationSeq',
                     'OrderCallbackPhoneNumber',
                     'OrderEnteredBy',
                     'OrderEntererLocation',
                     'OriginalAttributesSequence',
                     'OtherPatientIDs',
                     'OtherPatientIDsSeq',
                     'OtherPatientNames',
                     'OverlayDate',
                     'overlays',
                     'OverlayTime',
                     'PaletteColorLUTUID',
                     'ParticipantSequence',
                     'PatientAddress',
                     'PatientAge',
                     'PatientBirthDate',
                     'PatientBirthName',
                     'PatientBirthTime',
                     'PatientComments',
                     'PatientID',
                     'PatientIdentityRemoved',
                     'PatientInstitutionResidence',
                     'PatientInsurancePlanCodeSeq',
                     'PatientMotherBirthName',
                     'PatientName',
                     'PatientPhoneNumbers',
                     'PatientPrimaryLanguageCodeSeq',
                     'PatientPrimaryLanguageModifierCodeSeq',
                     'PatientReligiousPreference',
                     'PatientSex',
                     'PatientSexNeutered',
                     'PatientSize',
                     'PatientState',
                     'PatientTransportArrangements',
                     'PatientWeight',
                     'PerformedLocation',
                     'PerformedStationAET',
                     'PerformedStationGeoLocCodeSeq',
                     'PerformedStationName',
                     'PerformedStationNameCodeSeq',
                     'PerformingPhysicianIdSeq',
                     'PerformingPhysicianName',
                     'PerformProcedureStepEndDate',
                     'PersonAddress',
                     'PersonIdCodeSequence',
                     'PersonName',
                     'PersonTelephoneNumbers',
                     'PhysicianApprovingInterpretation',
                     'PhysicianOfRecord',
                     'PhysicianOfRecordIdSeq',
                     'PhysicianReadingStudyIdSeq',
                     'PlaceOrderNumberOfImagingServiceReq',
                     'PlateID',
                     'PPSDescription',
                     'PPSID',
                     'PPSStartDate',
                     'PPSStartTime',
                     'PregnancyStatus',
                     'PreMedication',
                     'ProjectName',
                     'ProtocolName',
                     'Radiopharmaceutical Information Sequence',
                     'Radiopharmaceutical Start DateTime',
                     'Radiopharmaceutical Stop DateTime',
                     'ReasonForImagingServiceRequest',
                     'ReasonforStudy',
                     'RefDigitalSignatureSeq',
                     'ReferencedFrameOfReferenceUID',
                     'ReferencedPatientAliasSeq',
                     'ReferringPhysicianAddress',
                     'ReferringPhysicianName',
                     'ReferringPhysicianPhoneNumbers',
                     'ReferringPhysiciansIDSeq',
                     'RefGenPurposeSchedProcStepTransUID',
                     'RefImageSeq',
                     'RefPatientSeq',
                     'RefPPSSeq',
                     'RefSOPClassUID',
                     'RefSOPInstanceMACSeq',
                     'RefSOPInstanceUID',
                     'RefStudySeq',
                     'RegionOfResidence',
                     'RelatedFrameOfReferenceUID',
                     'RequestAttributesSeq',
                     'RequestedContrastAgent',
                     'RequestedProcedureComments',
                     'RequestedProcedureDescription',
                     'RequestedProcedureID',
                     'RequestedProcedureLocation',
                     'RequestingPhysician',
                     'RequestingService',
                     'ResponsibleOrganization',
                     'ResponsiblePerson',
                     'ResultComments',
                     'ResultsDistributionListSeq',
                     'ResultsIDIssuer',
                     'ReviewerName',
                     'ScheduledHumanPerformersSeq',
                     'ScheduledPatientInstitutionResidence',
                     'ScheduledPerformingPhysicianIDSeq',
                     'ScheduledPerformingPhysicianName',
                     'ScheduledStationAET',
                     'ScheduledStationGeographicLocCodeSeq',
                     'ScheduledStationName',
                     'ScheduledStationNameCodeSeq',
                     'ScheduledStudyLocation',
                     'ScheduledStudyLocationAET',
                     'ScheduledStudyStartDate',
                     'SeriesDate',
                     'SeriesDescription',
                     'SeriesInstanceUID',
                     'SeriesTime',
                     'ServiceEpisodeDescription',
                     'ServiceEpisodeID',
                     'SiteID',
                     'SiteName',
                     'SmokingStatus',
                     'SoftwareVersion',
                     'SOPInstanceUID',
                     'SourceImageSeq',
                     'SpecialNeeds',
                     'SPSDescription',
                     'SPSEndDate',
                     'SPSEndTime',
                     'SPSLocation',
                     'SPSStartDate',
                     'SPSStartTime',
                     'StationName',
                     'StorageMediaFilesetUID',
                     'StructureSetDate',
                     'StudyArrivalDate',
                     'StudyComments',
                     'StudyCompletionDate',
                     'StudyDate',
                     'StudyDescription',
                     'StudyID',
                     'StudyIDIssuer',
                     'StudyInstanceUID',
                     'StudyTime',
                     'SynchronizationFrameOfReferenceUID',
                     'TemplateExtensionCreatorUID',
                     'TemplateExtensionOrganizationUID',
                     'TextComments',
                     'TextString',
                     'TimezoneOffsetFromUTC',
                     'TopicAuthor',
                     'TopicKeyWords',
                     'TopicSubject',
                     'TopicTitle',
                     'TransactionUID',
                     'TrialName',
                     'UID',
                     'VerifyingObserverIdentificationCodeSeq',
                     'VerifyingObserverName',
                     'VerifyingObserverSequence',
                     'VerifyingOrganization',
                     'VisitComments',
                     'VOILUTSequence',  # this field needed if you have problem with WW/WC
                     ]


def anonymize_dicom_files(dicom_files):
    for dicom_file in dicom_files:
        dataset = pydicom.dcmread(dicom_file)
        for dicom_field_name in DICOM_FIELD_NAMES:
            if dicom_field_name in dataset:
                delattr(dataset, dicom_field_name)
        file_name = os.path.basename(dicom_file)
        result_path = os.path.join(clean_dir, file_name)
        dataset.save_as(result_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='source_dir', type=str, help='source_directory')
    parser.add_argument(dest='target_dir', type=str, help='target_directory')

    args = parser.parse_args()

    ident_dir = args.ident_dir
    clean_dir = args.clean_dir
    del args.ident_dir
    del args.clean_dir

    dicom_files = [y for x in os.walk(ident_dir) for y in glob.glob(os.path.join(x[0], '*.dcm'))]

    anonymize_dicom_files(dicom_files)
