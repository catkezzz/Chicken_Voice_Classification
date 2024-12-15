package com.example.chickenapp

import android.Manifest
import android.app.AlertDialog
import android.os.Bundle
import android.content.pm.PackageManager
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.Toast
import android.widget.ImageButton
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.github.squti.androidwaverecorder.WaveRecorder
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.asRequestBody
import org.json.JSONObject
import java.io.File
import java.io.FileNotFoundException
import java.io.IOException
import java.nio.file.Files
import java.util.Timer
import java.util.TimerTask
import java.util.concurrent.TimeUnit

const val REQUEST_CODE = 200
class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient.Builder()
        .connectTimeout(10, TimeUnit.SECONDS)
        .writeTimeout(10, TimeUnit.SECONDS)
        .readTimeout(30, TimeUnit.SECONDS)
        .build()

    private lateinit var btnRecord: ImageButton
    private lateinit var btnInfo: ImageButton
    private lateinit var textViewPredict: TextView
    private lateinit var textViewConfidence: TextView
    private lateinit var textViewInfo: TextView
    private lateinit var recordNotice: TextView
    private lateinit var filePath: String
    private lateinit var waveRecorder: WaveRecorder
    private lateinit var handler: Handler
    private lateinit var waveFormview: WaveformView

    private var timer = Timer()
    private var isRecording = false
    private var permissions = arrayOf(Manifest.permission.RECORD_AUDIO)
    private var permissionGranted = false


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        permissionGranted = ActivityCompat.checkSelfPermission(
            this,
            permissions[0]
        ) == PackageManager.PERMISSION_GRANTED
        if (!permissionGranted)
            ActivityCompat.requestPermissions(this, permissions, REQUEST_CODE)

        btnRecord = findViewById(R.id.btnRecord)
        btnInfo = findViewById(R.id.btnInfo)
        textViewPredict = findViewById(R.id.textViewResult)
        textViewConfidence = findViewById(R.id.textViewConfidence)
        textViewInfo = findViewById(R.id.textViewInfo)
        recordNotice = findViewById(R.id.recordNotice)
        waveFormview = findViewById(R.id.waveformView)

        handler = Handler(Looper.getMainLooper())
        filePath = externalCacheDir?.absolutePath + "/audioFile.wav"
        waveRecorder = WaveRecorder(filePath)


        btnRecord.setOnClickListener {
            if (isRecording) {
                stopRecording()
                btnRecord.setImageResource(R.drawable.ic_mic)
                Toast.makeText(this, "Rekaman berhenti", Toast.LENGTH_SHORT).show()
                recordNotice.text = "Tekan untuk mulai rekam"
            } else {
                startRecording()
                btnRecord.setImageResource(R.drawable.ic_stop)
                Toast.makeText(this, "Rekaman dimulai", Toast.LENGTH_SHORT).show()
                recordNotice.text = "Tekan untuk berhenti rekam"
            }
        }
        btnInfo.setOnClickListener {
            showInfoDialog()
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)

        if (requestCode == REQUEST_CODE) {
            permissionGranted = grantResults[0] == PackageManager.PERMISSION_GRANTED
        }
    }

    private fun showInfoDialog() {
        val dialogView = layoutInflater.inflate(R.layout.dialog_info, null)

        val builder = AlertDialog.Builder(this)
        builder.setView(dialogView)
        builder.setCancelable(true)

        val dialog = builder.create()
        dialog.show()

        dialogView.setOnClickListener {
            dialog.dismiss()
        }
    }

    private fun startRecording() {
        if (!permissionGranted) {
            ActivityCompat.requestPermissions(this, permissions, REQUEST_CODE)
            return
        }
        isRecording = true
        waveRecorder.startRecording()
        waveRecorder.onAmplitudeListener = {
            waveFormview.addAmplitude("$it".toFloat())
        }
        timer = Timer()
        timer.schedule(object : TimerTask() {
            override fun run() {
                waveRecorder.stopRecording()
                handler.post {
                    val recordedFile = File(filePath)
                    val tempFile = Files.createTempFile(cacheDir.toPath(), "audioTemp", ".wav").toFile()
                    tempFile.deleteOnExit()
                    recordedFile.copyTo(tempFile, overwrite = true)
                    uploadFile(tempFile, textViewPredict, textViewConfidence)
                    try {
                        Log.i("FileCheck", "File name: ${recordedFile.name}")
                        Log.i("FileCheck", "File path: ${recordedFile.path}")
                        Log.i("FileCheck", "File size: ${recordedFile.length()} bytes")
                    } catch (e: FileNotFoundException) {
                        Log.e("FileCheck", e.message.toString())
                    }
                    waveRecorder.startRecording()
                }
            }
        }, 5000, 5000)
    }


    private fun uploadFile(file: File, predictionTextView: TextView, confidenceTextView: TextView) {

        val requestBody = MultipartBody.Builder()
            .setType(MultipartBody.FORM)
            .addFormDataPart("file", file.name, file.asRequestBody("audio/wav".toMediaTypeOrNull()))
            .build()

        val request = Request.Builder()
            .url("http://160.100.5.122:5000/predict")
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
                Log.e("UploadFile", "File upload failed: ${e.message}")
            }

            override fun onResponse(call: Call, response: Response) {
                response.body?.string()?.let { responseBody ->
                    runOnUiThread {
                        val json = JSONObject(responseBody)
                        val prediction = json.getString("prediction")
                        val confidence = json.getDouble("confidence")

                        when (prediction){
                            "Suara ayam pertanda bahaya" -> textViewInfo.text=
                                "Suara ini berfungsi untuk memperingatkan ayam lain di sekitarnya agar waspada dan siap melarikan diri atau bersembunyi."
                            "Suara ayam betina marah" -> textViewInfo.text=
                                "Suara ini dihasilkan oleh ayam betina ketika merasa terganggu atau terancam."
                            "Suara ayam betina memanggil jantan untuk kawin" -> textViewInfo.text=
                                "Suara ini adalah panggilan khas dari ayam betina untuk menunjukkan kesiapan betina untuk kawin"
                            "Suara ayam betina setelah bertelur" -> textViewInfo.text=
                                "Suara ini adalah cara ayam betina mengumumkan bahwa ia telah bertelur, memperingatkan ayam lain untuk menjaga telurnya dari bahaya"
                        }
                        predictionTextView.text = prediction
                        confidenceTextView.text = String.format("Confidence: %.2f%%", confidence)
                    }
                }
                Log.i("UploadFile", "File upload successful")
            }
        })
    }

    private fun stopRecording() {
        isRecording = false
        waveRecorder.stopRecording()
        timer.cancel()
    }
}
