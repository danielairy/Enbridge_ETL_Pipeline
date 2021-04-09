with FeatureClassCte as (
SELECT Code,
    CASE WHEN Width >= 3 * THICK And Length >= 3 * THICK Then 'General' ELSE
      CASE WHEN WIDTH>0 AND ((THICK <= Width And 6 * Width > Width) And ( THICK<= Length And 6 * THICK > Length) And (Length / Width > 0.5 And Length / Width < 2)) Then 'Pitting' ELSE
        CASE WHEN  WIDTH>0 AND (Width >= THICK And Width < 3 * THICK And Length / Width >= 2) Then 'Axial Grooving' ELSE
          CASE WHEN  WIDTH>0 AND (Length / Width <= 0.5 And THICK <= Length And Length < 3 * THICK) Then 'Circumferential Grooving' ELSE
            CASE WHEN (0 < Width And Width < THICK And 0 < Length And Length < THICK) Then 'Pinhole' ELSE
              CASE WHEN (0 < Width And Width < THICK And Length >= THICK) Then 'Axial Slotting' ELSE
                CASE WHEN (Width >= THICK And 0 < Length And Length < THICK) Then 'Circumferential Slotting' ELSE '' END
              END
            END
      END
        END
      END
    END FeatureClass
FROM IP_Objects F
Where Fea in ('Metal Loss')
  AND F.idSegment in (:SelectedPipelines) AND F.CodeInsp in (:SelectedRuns)
),



Main as (
SELECT DISTINCT 
       F.Code, 
       F.Code ID, 
       S_Segment.stNameShort as PipeIndex,
       F.idSegment, 
       F.nmStartMeter, 
       F.nmEndMeter, 
       CASE WHEN F.InspShortName IS NULL THEN 'MANUAL/REPAIR ANCHOR' ELSE F.InspShortName END as InspShortName, 
       F.FEA_NUM, 
       F.FEA_ORIGIN_ID, 
       F.GrShortName, 
       F.Fea, 
       F.Length, 
       F.Width, 
       F.Depth, 
       F.GirthWeld,

       F.[GW_Original_ID],
       PB.Joint_Number,
       PB.[LONG_SEAM_ORIENTATION],
       PB.nmWT, 

       F.DistFromPipeG as DistFromPipe, 
       F.Fea_AngleG, 
       F.FEA_ANGLE_HG, 
       F.MLProc, 
       '' ClusterMethodCL,

       F.Fea_lock_type, 
       F.CodeINSP, 
       S_Segment.stNameShort, 
       F.NOM_THICK, 
       F.THICK, 
       F.FEA_DISTANCE, 
       F.Prim, 
       CASE WHEN IP_Runs.D IS NULL THEN S_Segment.nmDiameter ELSE IP_Runs.D END * 25.4 AS D, 
       PB.SMYS SMYS, PB.SMTS SMTS, NULL SFLOW,  
       CAST(F.PipeGrade as NVarChar(20)) PipeGrade,
       FE."_F1", FE."_F2", FE."_F3", FE."_F4", FE."_F5", FE."_F6", FE."_F7", FE."_F8", FE."_F9", FE."_F10", FE."_F11", FE."_F12", FE."_F13", FE."_F14", FE."_F15", FE."_F16", FE."_F17", FE."_F18", FE."_F19", FE."_F20",
       FE."_F21", FE."_F22", FE."_F23", FE."_F24", FE."_F25", FE."_F26",

       F.AnomalyFlag

      ,[ToolTechnology]
      ,[DentStrain]
      ,[ClusterID]
      ,[LongSeamPosition]         
      ,[TotalVelocity]
      ,[DegradedData]

      ,[WidthTolerance]
      ,ISNULL([DepthTolerance], UNC.[Depth_Sizing_Accuracy]) [DepthTolerance] 
      ,ISNULL([LengthTolerance], UNC.[Length_Sizing_Accuracy]) [LengthTolerance] 
      ,CAST(CASE WHEN IsNumeric([GIS_CURRENT_MOP])=1 THEN CAST([GIS_CURRENT_MOP] as Float) ELSE NULL END as Float) Pmo

      ,FC.FeatureClass

      ,[PipelineMOP]
      ,[DistanceToUSGW]
      ,[DistanceToNextPipelineIndication]
      ,[FailurePressurePSI]
      ,[FailurePressureMethod]
      ,[RPR]
      ,F.[Elevation]

      ,R.RepairNumber, RT.Name AS MRA, 
       RS.NAME AS Status, 
       R.MAX_PRESS, R.NOTES, R.ID AS REPAIR_SYSKEY,
       F.wgsX, F.wgsY,
       CASE WHEN Year(IP_Runs.StartDate) - INSTALL_YEAR<=0 THEN NULL ELSE Year(IP_Runs.StartDate) - INSTALL_YEAR END Age,
       NDE.ID as NDE_ID

FROM IP_Objects F
     INNER JOIN S_Segment ON S_Segment.id = F.idSegment 
     LEFT JOIN RH_ASGD_REPAIR R
       LEFT JOIN IP_RepairTypes RT ON R.CMetRem = RT.Code
       LEFT JOIN D_RepairStatus RS ON R.RepairStatus=RS.Code
/*     ON F.nmStartMeter BETWEEN R.gb_R and R.ge_R and F.CodeInsp=R.RUN_ID and F.CodeUCH=R.SEGMENT_ID */
       LEFT JOIN RH_ASGD_REPAIR_DEF DE ON R.ID = DE.ASGD_REPAIR_ID
     ON DE.DEFECT_ID=F.Code  

     LEFT JOIN FeatureClassCte FC ON FC.Code=F.Code  
     LEFT JOIN [EGD_D_ToolsUncertainty] UNC ON UNC.[Tool_Type]=F.[ToolTechnology] AND FC.FeatureClass=UNC.[Anomaly_Dimension_Class]
     LEFT JOIN IP_Runs ON IP_Runs.SYSKEY = F.CodeInsp 
     LEFT JOIN IP_ObjectsExtension FE ON FE.id = F.Code 
     LEFT JOIN RH_SMYS ON RH_SMYS.Grade = F.PipeGrade 
     LEFT JOIN EGD_O_Pipebook PB ON F.idSegment=PB.idSegment AND F.nmStartMeter>=PB.nmStartMeter and F.nmStartMeter<PB.nmEndMeter    
     LEFT JOIN [IP_Excavation] NDE ON [PIMSFeatureID]=F.Code 
     LEFT JOIN GIS_PRIMPipelineInformation ON GIS_PRIMPipelineInformation.GIS_INDEX_=stNameShort  
Where F.idSegment in (:SelectedPipelines) AND F.CodeInsp in (:SelectedRuns)
),
withCorrosion as (
SELECT
      Code, idSegment,
      CAST(CASE WHEN NOT Age IS NULL THEN MLProc/Age ELSE NULL END as Float) CGRP, 
      CAST(CASE WHEN NOT Age IS NULL THEN MLProc*NOM_THICK/100/Age ELSE NULL END as Float) CGRD, 
      CAST(CASE WHEN NOT Age IS NULL THEN Length/Age ELSE NULL END as Float) CGRL, 
      CAST(CASE WHEN NOT Age IS NULL THEN Width/Age ELSE NULL END as Float) CGRW
FROM Main
WHERE Fea='Metal Loss' AND not MLProc Is Null
),
withAVGCorrosion as (
SELECT idSegment,        
      AVG(CGRP) AVG_CGRP, 
      AVG(CGRD) AVG_CGRD, 
      AVG(CGRL) AVG_CGRL, 
      AVG(CGRW) AVG_CGRW
FROM withCorrosion
GROUP BY idSegment
)



SELECT
      A.*,
      withCorrosion.CGRP, 
      withCorrosion.CGRD, 
      withCorrosion.CGRL, 
      withCorrosion.CGRW,
      withAVGCorrosion.AVG_CGRP, 
      withAVGCorrosion.AVG_CGRD, 
      withAVGCorrosion.AVG_CGRL, 
      withAVGCorrosion.AVG_CGRW,     
      MLProc + CGRP*7 MLProc7Y, 
      MLProc*NOM_THICK/100 + CGRD*7 Depth7Y, 
      Length + CGRL*7 Length7Y, 
      Width + CGRW*7 Width7Y 
FROM Main A 
LEFT JOIN withCorrosion ON withCorrosion.Code=A.Code
LEFT JOIN withAVGCorrosion ON withAVGCorrosion.idSegment=A.idSegment
Where A.idSegment in (:SelectedPipelines) AND A.CodeInsp in (:SelectedRuns)