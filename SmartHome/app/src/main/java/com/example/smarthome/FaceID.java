package com.example.smarthome;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

import androidx.activity.EdgeToEdge;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.storage.FirebaseStorage;
import com.google.firebase.storage.ListResult;
import com.google.firebase.storage.StorageReference;

import java.util.ArrayList;
import java.util.List;

public class FaceID extends AppCompatActivity {

    FirebaseStorage storage = FirebaseStorage.getInstance();
    StorageReference storageRef = storage.getReference().child("images");

    FirebaseDatabase database = FirebaseDatabase.getInstance();
    DatabaseReference change_image = database.getReference("change_image");
    DatabaseReference delete_image = database.getReference("delete_image");

    public static Item get_item(String name,String imageUrl){
        String[] subName = (name.split("\\."))[0].split("_");

        return new Item(subName[0],imageUrl,subName[1]);
    }
    public static String get_name(Item item){
        return  item.getName() + "_" + item.getId() + ".jpg";
    }

    ImageButton back_main;
    ImageButton add_face;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        EdgeToEdge.enable(this);
        setContentView(R.layout.activity_face_id);
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
            Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
            return insets;
        });

        back_main = findViewById(R.id.back_main);
        add_face = findViewById(R.id.add_face);

        back_main.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent  = new Intent(FaceID.this , MainActivity.class);
                startActivity(intent);
            }
        });
        add_face.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(FaceID.this, add_face.class);
                startActivity(intent);
            }
        });

        RecyclerView recyclerView = findViewById(R.id.recyclerView);
        List<Item> items = new ArrayList<Item>();
        MyApdapter adapter = new MyApdapter(getApplicationContext(), items);

        storageRef.listAll().addOnSuccessListener(new OnSuccessListener<ListResult>() {
            @Override
            public void onSuccess(ListResult listResult) {
                List<StorageReference> imageRefernce = listResult.getItems();
                for (StorageReference imageRef : imageRefernce){
                    imageRef.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
                        @Override
                        public void onSuccess(Uri uri) {
                            String imageUrl = uri.toString();
                            items.add(get_item(imageRef.getName(),imageUrl));
                            adapter.notifyDataSetChanged();
                        }
                    });
                }
            }
        });

        change_image.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot snapshot) {
                Integer val = snapshot.getValue(Integer.class);
                if (val == 1){
                    items.clear();
                    storageRef.listAll().addOnSuccessListener(new OnSuccessListener<ListResult>() {
                        @Override
                        public void onSuccess(ListResult listResult) {
                            List<StorageReference> imageRefernce = listResult.getItems();
                            if (imageRefernce.isEmpty()){
                                adapter.notifyDataSetChanged();
                                change_image.setValue(0);
                            } else
                                for (StorageReference imageRef : imageRefernce){
                                    imageRef.getDownloadUrl().addOnSuccessListener(new OnSuccessListener<Uri>() {
                                        @Override
                                        public void onSuccess(Uri uri) {
                                            String imageUrl = uri.toString();
                                            items.add(get_item(imageRef.getName(),imageUrl));
                                            change_image.setValue(0);
                                            adapter.notifyDataSetChanged();
                                        }
                                    });
                                }
                        }
                    });
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError error) {

            }
        });

        adapter.setOnItemClickListener(new MyApdapter.OnItemClickListener() {
            @Override
            public void onDeleteClick(int position) {
                String name_delete = get_name(items.get(position));
                delete_image.setValue(name_delete);
                storageRef.child(name_delete).delete().addOnSuccessListener(new OnSuccessListener<Void>() {
                    @Override
                    public void onSuccess(Void unused) {
                        change_image.setValue(1);
                    }
                });
            }
        });

        recyclerView.setLayoutManager(new LinearLayoutManager(this));
        recyclerView.setAdapter(adapter);
    }
}